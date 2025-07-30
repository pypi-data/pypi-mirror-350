import inspect
from typing import List

from django_post_api.fields import ModelField
from django_post_api.params import BaseParam
from django_post_api.helpers import merge_two_field_list


class DocMixin(object):
    # 定义排序规则
    @staticmethod
    def sort_key(api_name):
        prefix_order = {'post': 1, 'get_page': 2, 'get_all': 3, 'get_tree': 4, 'get_detail': 5, 'put': 6, 'delete': 7}
        for prefix, order in prefix_order.items():
            if api_name.startswith(prefix):
                return order
        return float('inf')  # 如果没有匹配到任何前缀，则放在最后


def get_docstring(target):
    try:
        return inspect.getdoc(target) or None
    except Exception as e:
        return None


class ShowDocMixin(DocMixin):
    name = None

    @classmethod
    def get_showdoc_content(cls):
        func_list = []
        for func_name in dir(cls):
            if func_name.endswith("_api") or func_name == "get":
                func_list.append(func_name)

        showdoc_list = []
        sorted_func_name_list = sorted(func_list, key=cls.sort_key)
        for func_name in sorted_func_name_list:
            act = func_name.replace('_api', '')
            act_name = get_docstring(getattr(cls, func_name)) or act

            field_list: List[ModelField] = []
            params_list: List[BaseParam] = []
            if func_name in ["get_page_api", "get_all_api", "get_detail_api"]:
                if func_name == "get_page_api":
                    params_list += getattr(cls, "page_query_params_list", [])
                    params_list += getattr(cls, "pagination_params_list", [])
                    params_list += getattr(cls, "order_by_params_list", [])
                    field_list += getattr(cls, "page_field_list", [])
                elif func_name == "get_all_api":
                    params_list += getattr(cls, "page_query_params_list", [])
                    params_list += getattr(cls, "order_by_params_list", [])
                    field_list += getattr(cls, "page_field_list", [])
                elif func_name == "get_detail_api":
                    params_list = getattr(cls, "detail_query_params_list", [])
                    page_field_list = getattr(cls, "page_field_list", [])
                    detail_field_list = getattr(cls, "detail_field_list", [])
                    field_list = merge_two_field_list(page_field_list, detail_field_list)
                elif func_name == "get_tree_api":
                    params_list = getattr(cls, "page_query_params_list", [])
            elif func_name == "post_api":
                params_list += getattr(cls, "post_params_list", [])
                params_list += getattr(cls, "post_many_to_many_params_list", [])
                params_list += getattr(cls, "post_related_many_to_many_params_list", [])
            elif func_name == "put_api":
                params_list += getattr(cls, "put_select_params_list", [])
                params_list += getattr(cls, "put_params_list", [])
                params_list += getattr(cls, "put_many_to_many_params_list", [])
                params_list += getattr(cls, "put_related_many_to_many_params_list", [])
            elif func_name == "delete_api":
                params_list += getattr(cls, "delete_params_list", [])
            elif func_name == "export_api":
                params_list += getattr(cls, "page_query_params_list", [])
            else:
                params_list += getattr(cls, f"{act}_params_list", [])
                field_list += getattr(cls, f"{act}_field_list", [])

            param_str_list = []
            for inx, param in enumerate(params_list):
                param_str_list.append(
                    param.get_showdoc_str(is_last=inx == len(params_list) - 1).lstrip("\n").rstrip("\n"))
            params_show_str = "\n".join(param_str_list)
            if params_show_str:
                params_show_str = f"\n{params_show_str}"

            return_str_list = []
            for inx, field in enumerate(field_list):
                return_str_list.append(
                    field.get_showdoc_str(is_last=inx == len(field_list) - 1).lstrip("\n").rstrip("\n")
                )
            if len(return_str_list) > 0:
                return_str = "\n".join(return_str_list)
                return_str = f"""返回字段
```
{{
{return_str}
}}
```
"""
            else:
                return_str = ""

            act_param = f'\t"act": "{act}", // 固定值' if func_name != "get" else ""
            showdoc_str = f"""#### {act_name}
请求参数
```
{{
{act_param}{params_show_str}
}}
```
{return_str}
"""
            showdoc_list.append(showdoc_str)
        return "\n\n".join(showdoc_list)
