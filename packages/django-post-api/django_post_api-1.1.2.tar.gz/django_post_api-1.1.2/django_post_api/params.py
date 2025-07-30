import datetime
from typing import Optional

from django.core.files.uploadedfile import UploadedFile

from .constants import DateTimeFormatEnum
from .errors import MyError


def param_query_fun(query_way: str):
    return lambda param_self, value: {f"{param_self.name}{query_way}": value}


class BaseParam(object):
    allow_type_list = []  # 允许的参数类型列表

    def __init__(self,
                 name: Optional[str] = None,
                 desc: Optional[str] = None,
                 not_allow_null: bool = False,
                 default_value=None,
                 query_fun=None,
                 length: Optional[int] = None,
                 min_value: Optional = None,
                 max_value: Optional = None,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 list_element=None,
                 dict_key_list=None,
                 choice_list=None,
                 model_field=None,
                 datetime_format: Optional[DateTimeFormatEnum] = None,
                 is_foreign: bool = False,
                 is_many_to_many: bool = False,
                 reverse=None,
                 ):
        if name:
            self.name = name
        elif model_field:
            if reverse:
                self.name = model_field.field._related_name
            else:
                self.name = model_field.field.name
        else:
            self.name = None
        if desc:
            self.desc = desc
        elif model_field:
            self.desc = model_field.field.verbose_name
        else:
            self.desc = self.name
        self.model_field = model_field
        self.not_allow_null = not_allow_null
        self.default_value = default_value
        self.query_fun = query_fun
        self.min_value = min_value
        self.max_value = max_value
        self.length = length
        self.min_length = min_length
        self.max_length = max_length
        self.list_element = list_element
        self.dict_key_list = dict_key_list
        self.choice_list = choice_list
        self.datetime_format = datetime_format
        self.is_foreign = is_foreign
        self.is_many_to_many = is_many_to_many
        self.reverse = reverse
        if self.list_element is not None:
            self.list_element.desc = self.desc
        # 验证提供的长度参数是否合理
        if self.length is not None and (self.min_length is not None or self.max_length is not None):
            raise ValueError("不能同时设置 'length' 和 'min_length' 或 'max_length'")
        if self.min_length is not None and self.max_length is not None and self.min_length > self.max_length:
            raise ValueError("'min_length' 不能大于 'max_length'")

    @property
    def show_name(self):
        return self.desc or self.name

    def extra_check_value(self, value):
        """额外的检验方法"""
        return value

    # def get_value(self, data):
    #     self.value = data.get(self.name, self.default_value)

    def check_value_length(self, value):
        if value is not None and (
                self.length is not None or self.min_length is not None or self.max_length is not None):
            value_len = len(value)
            if self.length is not None and value_len != self.length:
                raise MyError("请输入{}位的{}参数".format(self.length, self.show_name))
            if self.min_length is not None and value_len < self.min_length:
                raise MyError("{}参数需要不能少于{}位".format(self.show_name, self.min_length))
            if self.max_length is not None and value_len > self.max_length:
                raise MyError("{}参数需要不能多于{}位".format(self.show_name, self.max_length))

        return value

    def check_value_type(self, value):
        if self.allow_type_list and any(map(lambda x: isinstance(value, x), self.allow_type_list)) is False:
            raise MyError("{}参数类型错误".format(self.show_name))

    def check_value_choices(self, value):
        if value is not None and self.choice_list is not None:
            if value not in [choice['value'] for choice in self.choice_list]:
                raise MyError("{}参数不在可选范围内".format(self.show_name))

    def check_value_min_max_value(self, value):
        if value is not None and self.min_value is not None and value < self.min_value:
            raise MyError("{}参数超过允许的最小值".format(self.show_name))
        if value is not None and self.max_value is not None and value > self.max_value:
            raise MyError("{}参数超过允许的最大值".format(self.show_name))
        return value

    def base_check_param_value(self, value):
        if self.not_allow_null and value is None:
            raise MyError("{}参数不允许为空".format(f"{self.show_name}({self.name})"))
        if value is not None:
            self.check_value_type(value)
            self.check_value_length(value)
            self.check_value_min_max_value(value)
            self.check_value_choices(value)
        value = self.extra_check_value(value)
        res = {}
        if value is not None:
            if self.query_fun:
                value = self.query_fun(self, value)
                return value
            if self.name:
                if self.is_foreign:
                    for f_key, f_value in value.items():
                        if f_value:
                            if f_key == "id":
                                res[f"{self.name}_{f_key}"] = f_value
                            else:
                                res[f"{self.name}__{f_key}"] = f_value
                elif self.is_many_to_many:
                    for f_key, f_value in value.items():
                        if f_value:
                            res[f"{self.name}__{f_key}"] = f_value
                else:
                    res[self.name] = value
            else:
                return value
        return res

    def check_param_value(self, param_dict):
        param_value = param_dict.get(self.name, self.default_value)
        return self.base_check_param_value(param_value)

    def get_hint_value(self):
        return ""

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        name_str = f"""\"{self.name}\": """ if self.name else ""
        param_memo = self.get_param_memo().strip()
        return f"""{start_str}{name_str}{self.get_hint_value()} {',' if not is_last else ''} {f" // {param_memo}" if param_memo else ""}"""

    def get_param_memo(self):
        allow_null_name = "" if self.not_allow_null is False else "不可为空"
        if self.choice_list:
            one_choice_str = [f"{choice['label']}: {choice['value']}" for choice in self.choice_list]
            choice_str = f"可选值：{' 、'.join(one_choice_str)}"
        else:
            choice_str = ""
        return f"{allow_null_name} {self.desc if self.name and self.desc else ''} {choice_str}"

    def __str__(self):
        return self.name


class IntParam(BaseParam):
    allow_type_list = [int, str]

    def get_hint_value(self):
        return 1

    def extra_check_value(self, value):
        return int(value) if value else value


class FloatParam(BaseParam):
    allow_type_list = [float, int, str]

    def get_hint_value(self):
        return 1.0

    def extra_check_value(self, value):
        return float(value) if value else value


class StrParam(BaseParam):
    allow_type_list = [str]

    def get_hint_value(self):
        return f"""\"str\""""


class BoolParam(BaseParam):
    allow_type_list = [bool, ]

    def get_hint_value(self):
        return f"""true"""


class ListParam(BaseParam):
    allow_type_list = [list, ]

    def extra_check_value(self, value):
        if value is not None:
            new_list = []
            for inx, v in enumerate(value):
                new_v = self.list_element.base_check_param_value(v)
                new_list.append(new_v)
            value = new_list
        return value

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        t_count += 1
        hint_value = self.list_element.get_showdoc_str(t_count, is_last=True)
        return f"""
{start_str}"{self.name}": [ // {self.get_param_memo()}
{hint_value}
{start_str}]{',' if not is_last else ''} 
"""


class DictParam(BaseParam):
    """
    dict_key_list is must_has_value arg
    """
    allow_type_list = [dict, ]

    def extra_check_value(self, value) -> dict:
        if value:
            result = {}
            for dict_arg in self.dict_key_list:
                result.update(dict_arg.base_check_param_value(value.get(dict_arg.name)))
            value = result
        return value

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        t_count += 1
        child_str_list = []
        for inx, param in enumerate(self.dict_key_list):
            child_str_list.append(param.get_showdoc_str(t_count, is_last=inx == len(self.dict_key_list) - 1))
        child_str = '\n'.join(child_str_list)
        name_str = f""""{self.name}":""" if self.name else ""
        return f"""{start_str}{name_str}{{ //  {self.get_param_memo()}
{child_str}
{start_str}}}{',' if not is_last else ''} """


class DateTimeParam(StrParam):

    def extra_check_value(self, value):
        if self.datetime_format is None:
            raise MyError("{}参数未指定格式".format(self.show_name))
        if value:
            try:
                value = datetime.datetime.strptime(value, self.datetime_format.value)
            except ValueError:
                raise MyError("{}参数格式错误".format(self.show_name))
        return value

    def get_hint_value(self):
        if self.datetime_format is None:
            raise MyError("{}参数未指定格式".format(self.show_name))
        return f"""\"{datetime.datetime(2025, 1, 18).strftime(self.datetime_format.value)}\""""


class FileParam(BaseParam):
    type_list = [UploadedFile]

    def get_hint_value(self):
        return """文件，需要使用form表单上传"""

    # def __init__(self, allowed_extensions=None, max_size=None, *args, **kwargs):
    #     """
    #     :param allowed_extensions: 允许的文件扩展名列表
    #     :param max_size: 允许的最大文件大小（以M为单位）
    #     """
    #     super().__init__(*args, **kwargs)
    #     self.allowed_extensions = allowed_extensions
    #     self.max_size = max_size
    #
    # def extra_check_value(self, value: UploadedFile, parent_field=None):
    #     if not value:
    #         return value
    #
    #     # 检查文件扩展名
    #     if self.allowed_extensions:
    #         ext = value.name.split('.')[-1]  # 获取文件扩展名
    #         if ext.lower() not in self.allowed_extensions:
    #             raise ValueError(f"{self.get_desc(parent_field)}: 文件类型不允许")
    #
    #     # 检查文件大小
    #     if self.max_size and value.size > self.max_size * 1024 * 1024:
    #         raise ValueError(f"{self.get_desc(parent_field)}: 文件大小超过限制")
    #
    #     return value
