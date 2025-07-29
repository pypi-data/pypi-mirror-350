import json
from decimal import Decimal
from functools import wraps
from typing import List, Optional

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.views import View

from django_post_api.doc import ShowDocMixin
from django_post_api.errors import MyError
from django_post_api.fields import ModelField, ForeignKeyField, ManyToManyField, AnnotateField, BaseReturnField, \
    ModelFuncField
from django_post_api.helpers import build_tree_data, merge_two_field_list
from django_post_api.params import IntParam, BaseParam, ListParam


class DecimalJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def once_per_request(f):
    """装饰器：确保方法在一个请求周期内只被调用一次"""

    @wraps(f)
    def wrapped(instance):
        attr_name = f'_cached_{f.__name__}'
        if not hasattr(instance, attr_name):
            setattr(instance, attr_name, f(instance))
        return getattr(instance, attr_name)

    return wrapped


class BaseAPIView(View, ShowDocMixin):
    model = None
    default_need_token = False

    @staticmethod
    def check_params_list(params_data, params_list: list[BaseParam]):
        res = {}
        for param in params_list:
            value = param.check_param_value(params_data)
            res.update(value)
        return res

    @staticmethod
    def check_many_to_many_params_list(params_data, params_list: List[BaseParam]) -> dict:
        res = {}
        for params in params_list:
            param_value = params.check_param_value(params_data)
            for key, value in param_value.items():
                res[key] = {
                    "id_list": [data['id'] for data in value if "id" in data.keys()],
                    "data_list": [data for data in value if "id" not in data.keys()],
                }
        return res

    @staticmethod
    def set_many_to_many(obj, many_to_many_kwargs):
        if len(many_to_many_kwargs.keys()) > 0:
            for key, item in many_to_many_kwargs.items():
                manager = getattr(obj, key)
                id_list = item.get("id_list", [])
                data_list = item.get("data_list", [])
                if data_list:
                    for data in data_list:
                        new_instance = manager.model.objects.create(**data)
                        id_list.append(new_instance.id)
                if id_list:
                    manager.set(id_list)

    @staticmethod
    def check_related_many_to_many_params_list(params_data, params_list) -> dict:
        res = {}
        for params in params_list:
            param_value = params.check_param_value(params_data)
            for key, value in param_value.items():
                res[params.name] = {
                    "model": params.model_field.field.model,
                    "field_name": params.model_field.field.name,
                    "id_list": [data['id'] for data in value if "id" in data.keys()],
                    "data_list": [data for data in value if "id" not in data.keys()],
                }
        return res

    @staticmethod
    def set_related_many_to_many(obj, related_many_to_many_kwargs):
        if len(related_many_to_many_kwargs.keys()) > 0:
            for key, value in related_many_to_many_kwargs.items():
                model = value.get("model", None)
                field_name = value.get("field_name", None)
                id_list = value.get("id_list", [])
                data_list = value.get("data_list", [])
                create_list = []
                for data in data_list:
                    data[field_name] = obj
                    create_list.append(model(**data))
                model.objects.filter(**{f"{field_name}": obj}).exclude(id__in=id_list).delete()
                model.objects.bulk_create(create_list)

    @property
    @once_per_request
    def request_data(self):
        if self.request.content_type == "application/json":
            return json.loads(self.request.body)
        else:
            data_dict = {}
            for key in self.request.POST:
                values = self.request.POST.getlist(key)
                data_dict[key] = values if len(values) > 1 else values[0]
            # 从 request.FILES 获取数据
            for key in self.request.FILES:
                uploaded_files = self.request.FILES.getlist(key)
                data_dict[key] = uploaded_files if len(uploaded_files) > 1 else uploaded_files[0]
            return data_dict

    @property
    @once_per_request
    def request_act(self):
        return self.request_data.pop("act", None)

    def act_api_method_not_allowed(self):
        raise MyError(f"{self.request_act}方法未定义")

    def check_token(self):
        pass

    def pre_process_data(self):
        # 预处理一些数据，放到self上
        pass

    def post(self, request, *args, **kwargs):
        self.pre_process_data()
        handle = getattr(self, f"{self.request_act}_api", self.act_api_method_not_allowed)
        need_token = getattr(handle, "need_token",
                             getattr(self, f"{self.request_act}_need_token",
                                     getattr(self, "default_need_token", False)))
        if need_token:
            self.check_token()
        return handle()

    def base_return(self, return_data, status=200):
        return JsonResponse(return_data, status=status, encoder=DecimalJSONEncoder)

    def success_return(self, data=None, status=200, **kwargs):
        if data is None:
            data = {}
        return_data = {
            "err_msg": "ok",
            "data": data,
        }
        if kwargs:
            return_data.update(**kwargs)
        return self.base_return(return_data, status=status)

    def error_return(self, errmsg, status=500):
        return_data = {
            "err_msg": errmsg,
            "data": None,
        }
        return self.base_return(return_data, status=status)


class BaseAPIGetView(BaseAPIView):
    page_field_list: List[ModelField] = []

    order_by_params_list = [
        # StrParam(name="order_by")
    ]

    @property
    def order_by_params(self) -> list:
        params = self.check_params_list(self.request_data, self.order_by_params_list)
        order_by = params.get("order_by", None)
        if order_by is None:
            order_by = ["-id", ]
        return order_by

    page_query_params_list: List[BaseParam] = []

    @property
    def query_params(self) -> dict:
        return self.check_params_list(self.request_data, self.page_query_params_list)

    def get_queryset(self):
        return ModelToJson(model=self.model).get_queryset()


class APIGetAllView(BaseAPIGetView):

    def get_list_data_res(self):
        return ModelToJson(model=self.model).get_data_list(
            self.get_queryset(), self.page_field_list, query_params=self.query_params,
            order_by_params=self.order_by_params)

    def get_list_api(self):
        """获取全部列表数据"""
        res = self.get_list_data_res()
        return self.success_return(res)


class APIGetPageView(BaseAPIGetView):
    pagination_params_list = [
        IntParam(name="offset", default_value=0, min_value=0),
        IntParam(name="limit", default_value=20, max_value=100, min_value=1),
        # IntParam(name="page_number", desc="当前显示的页码", min_value=1, default_value=1),
        # IntParam(name="page_size", desc="每页显示的数量", min_value=1, max_value=100, default_value=20),
    ]

    def get_page_data_res(self):
        pagination_params = self.check_params_list(self.request_data, self.pagination_params_list)
        return ModelToJson(model=self.model).get_data_list(
            self.get_queryset(), self.page_field_list,
            query_params=self.query_params, order_by_params=self.order_by_params,
            offset=pagination_params.get("offset"), limit=pagination_params.get("limit"))

    def get_page_api(self):
        """获取列表分页数据"""
        res = self.get_page_data_res()
        return self.success_return(res)


class APIGetDetailView(BaseAPIGetView):
    detail_field_list: List[ModelField] = []

    detail_query_params_list = [
        IntParam(name="id", not_allow_null=True),
    ]

    def get_queryset(self):
        return ModelToJson(model=self.model).get_queryset()

    @property
    def detail_query_params(self) -> dict:
        return self.check_params_list(self.request_data, self.detail_query_params_list)

    def get_detail_data_res(self):
        field_list = merge_two_field_list(self.page_field_list, self.detail_field_list)
        return ModelToJson(model=self.model).get_data_list(
            self.get_queryset(), field_list=field_list,
            query_params=self.detail_query_params, order_by_params=self.order_by_params)

    def get_detail_api(self):
        """获取详情数据"""
        res = self.get_detail_data_res()
        data_list = res.get("data_list", [])
        if len(data_list) == 0:
            data = None
        else:
            data = data_list[0]
        return self.success_return(data)


class APIGetTreeView(APIGetAllView):

    def get_tree_api(self):
        """获取树形结构数据"""
        res = self.get_data_res()
        data_list = build_tree_data(res.get("data_list", []))
        return self.success_return(data_list, count=res.get("count", None))


class APIPostView(BaseAPIView):
    post_params_list: List[BaseParam] = []
    post_many_to_many_params_list: List[BaseParam] = []
    post_related_many_to_many_params_list: List[BaseParam] = []

    def post_db_operation(self, params):
        return self.model.objects.create(**params)

    def after_post(self, obj):
        pass

    @property
    def post_params(self) -> dict:
        return self.check_params_list(self.request_data, self.post_params_list)

    @property
    def post_many_to_many_params(self) -> dict:
        return self.check_many_to_many_params_list(self.request_data, self.post_many_to_many_params_list)

    @property
    def post_related_many_to_many_params(self) -> dict:
        return self.check_related_many_to_many_params_list(self.request_data,
                                                           self.post_related_many_to_many_params_list)

    def update_post_params_by_many_to_many(self, post_params, post_many_to_many_params,
                                           post_related_many_to_many_params):
        pass

    def handle_post(self):
        post_params = self.post_params
        post_many_to_many_params = self.post_many_to_many_params
        post_related_many_to_many_params = self.post_related_many_to_many_params
        self.update_post_params_by_many_to_many(post_params, post_many_to_many_params, post_related_many_to_many_params)
        with transaction.atomic():
            obj = self.post_db_operation(post_params)
            if post_many_to_many_params is not None:
                self.set_many_to_many(obj, post_many_to_many_params)
            if post_related_many_to_many_params is not None:
                self.set_related_many_to_many(obj, post_related_many_to_many_params)
        self.after_post(obj)
        return obj

    def post_api(self):
        """创建"""
        obj = self.handle_post()
        return self.success_return({"id": obj.id} if obj else None)


class APIPutView(BaseAPIView):
    put_select_params_list = [
        IntParam(name="id", not_allow_null=True, desc="需要修改的id"),
    ]
    put_params_list: List[BaseParam] = []
    put_many_to_many_params_list: List[BaseParam] = []
    put_related_many_to_many_params_list: List[BaseParam] = []

    @property
    def put_select_params(self):
        return self.check_params_list(self.request_data, self.put_select_params_list)

    @property
    def put_params(self):
        return self.check_params_list(self.request_data, self.put_params_list)

    @property
    def put_many_to_many_params(self) -> dict:
        return self.check_many_to_many_params_list(self.request_data, self.put_many_to_many_params_list)

    @property
    def put_related_many_to_many_params(self):
        return self.check_related_many_to_many_params_list(self.request_data,
                                                           self.put_related_many_to_many_params_list)

    def put_db_operation(self, put_select_params, put_params) -> int:
        return self.model.objects.active().filter(**put_select_params).update(**put_params)

    def after_put(self):
        pass

    def handle_put(self, put_select_params, put_params, put_many_to_many_params=None,
                   put_related_many_to_many_params=None) -> int:
        if len(put_select_params.keys()) == 0:
            raise MyError("查询参数不可为空")
        if len(put_params.keys()) == 0:
            raise MyError("修改参数不可为空")
        with transaction.atomic():
            count = self.put_db_operation(put_select_params, put_params)
            if any([put_many_to_many_params, put_related_many_to_many_params]):
                for obj in self.model.objects.filter(**put_select_params).only("id").iterator():
                    if put_many_to_many_params is not None:
                        self.set_many_to_many(obj, put_many_to_many_params)
                    if put_related_many_to_many_params is not None:
                        self.set_related_many_to_many(obj, put_related_many_to_many_params)
        self.after_put()
        return count

    def put_api(self):
        """修改"""
        count = self.handle_put(self.put_select_params, self.put_params, self.put_many_to_many_params,
                                self.put_related_many_to_many_params)
        return self.success_return({"count": count})


class APIDeleteView(BaseAPIView):
    delete_params_list = [
        IntParam(name="id", desc="需要删除的id，与id_list参数二选一，不可同时为空"),
        ListParam(name="id_list", list_element=IntParam(), desc="需要删除的id列表，与id参数二选一，不可同时为空"),
    ]

    @property
    def delete_params(self) -> dict:
        delete_params = self.check_params_list(self.request_data, self.delete_params_list)
        delete_id = delete_params.pop("id", None)
        delete_id_list = delete_params.pop("id_list", None)
        if delete_id:
            delete_params['id'] = delete_id
        if delete_id_list:
            delete_params['id__in'] = delete_id_list
        return delete_params

    def delete_db_operation(self):
        return self.model.objects.active().filter(**self.delete_params).delete()

    def handle_delete(self):
        _ = self.delete_params
        if len(self.delete_params.keys()) == 0:
            raise MyError("删除参数不可为空")
        with transaction.atomic():
            count = self.delete_db_operation()
        return count

    def delete_api(self):
        """删除"""
        count = self.handle_delete()
        return self.success_return({"count": count})


class APITableView(APIGetPageView, APIGetAllView, APIGetDetailView, APIPostView, APIPutView, APIDeleteView):
    pass


class ModelToJson:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def __get_related_list(all_field_list) -> list:
        data_list = []
        for field in all_field_list:
            if isinstance(field, ForeignKeyField):
                data_list.extend(field.get_related_list())
            elif isinstance(field, ManyToManyField):
                data_list.extend(field.get_related_list(is_prefetch=True))
            else:
                continue
        return data_list

    @staticmethod
    def __get_only_field_name_list(all_field_list) -> list:
        data_list = []

        def process_field(_field, prefix=""):
            if isinstance(_field, ForeignKeyField):
                # 递归处理 ForeignKeyField 的 field_list
                for sub_field in _field.related_field_list:
                    new_prefix = f"{prefix}{_field.name}__" if prefix else f"{_field.name}__"
                    process_field(sub_field, new_prefix)
            elif isinstance(_field, ManyToManyField):
                return  # 忽略 ManyToManyField
            elif isinstance(_field, ModelFuncField):
                return  # 忽略 ModelFuncField
            elif isinstance(_field, ModelField):
                data_list.append(f"{prefix}{_field.name}" if prefix else _field.name)
            elif isinstance(_field, AnnotateField):
                return  # 忽略 AnnotateField

        for field in all_field_list:
            process_field(field)
        return data_list

    def get_queryset(self):
        return self.model.objects.active()

    def get_data_list(self, queryset, field_list: List[BaseReturnField],
                      # detail_field_list: List[BaseReturnField] = None,
                      query_params: Optional[dict] = None, exclude_params: Optional[dict] = None,
                      order_by_params: Optional[list] = None, offset: Optional[int] = None,
                      limit: Optional[int] = None) -> dict:
        # if detail_field_list:
        #     all_field_list = merge_two_field_list(field_list, detail_field_list)
        # else:
        #     all_field_list = field_list
        annotate_res = {}
        for field in field_list:
            if isinstance(field, AnnotateField):
                annotate_res[field.out_name] = field.annotate_func(self)
        if annotate_res:
            queryset = queryset.annotate(**annotate_res)

        if query_params is not None:
            for key, value in query_params.items():
                if isinstance(value, Q):
                    queryset = queryset.filter(value)
                else:
                    queryset = queryset.filter(**{key: value})
        if exclude_params is not None:
            queryset = queryset.exclude(**exclude_params)

        related_list = self.__get_related_list(field_list)
        if related_list:
            select_related_list = []
            prefetch_related_list = []
            for related in related_list:
                if isinstance(related, Prefetch):
                    prefetch_related_list.append(related)
                elif isinstance(related, str):
                    select_related_list.append(related)
            if select_related_list:
                queryset = queryset.select_related(*select_related_list)
            if prefetch_related_list:
                queryset = queryset.prefetch_related(*prefetch_related_list)

        model_field_list = self.__get_only_field_name_list(field_list)
        queryset = queryset.only(*model_field_list)
        if order_by_params:
            queryset = queryset.order_by(*order_by_params)
        data_list = []
        if all(i is not None for i in [offset, limit]):
            page_queryset = queryset[offset:offset + limit]
        else:
            page_queryset = queryset
        for obj in page_queryset:
            one_data = {"id": obj.id}
            for field in field_list:
                one_data.update(field.get_field_value(obj))
            data_list.append(one_data)
        return {
            "total": queryset.count(),
            "data_list": data_list,
        }

    def get_detail(self, queryset, field_list: List[BaseReturnField],
                   query_params: Optional[dict] = None, exclude_params: Optional[dict] = None,
                   order_by_params: Optional[list] = None) -> Optional[dict]:
        res = self.get_data_list(queryset=queryset, field_list=field_list, query_params=query_params,
                                 exclude_params=exclude_params, order_by_params=order_by_params)
        data_list = res.get("data_list", [])
        if len(data_list) == 0:
            return None
        return data_list[0]
