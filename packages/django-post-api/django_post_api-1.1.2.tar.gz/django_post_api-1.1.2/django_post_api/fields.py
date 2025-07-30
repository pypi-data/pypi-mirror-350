from django.db.models import Prefetch
from django.db.models.fields.related import ForeignKey as RelatedForeignKey

from django_post_api.errors import MyError


class BaseReturnField(object):
    def __init__(self,
                 model_field=None,
                 name=None, label=None,
                 out_name=None, value=None,
                 annotate_func=None,
                 model_func=None,
                 datetime_format=None,
                 related_field_list=None,
                 reverse=None,
                 queryset=None,
                 limit_num=None,
                 ):
        if name is None:
            if model_field:
                name = model_field.field.name
                if reverse:
                    related_name = model_field.field._related_name
                    if related_name is None:
                        raise MyError(f"请给关联的字段{name}设置一个 'related_name'")
                    name = related_name
            else:
                raise MyError("'name' 和 'model_field' 不能同时为空")
        self.name = name  # 字段 名称
        self.out_name = out_name if out_name else name
        if label is None:
            if model_field:
                label = model_field.field.verbose_name
            else:
                label = self.out_name
        self.label = label
        self.value = value  # 自定义值
        self.annotate_func = annotate_func  # 自定义值
        self.model_func = model_func  # 自定义值
        self.model_field = model_field  # 自定义值
        self.datetime_format = datetime_format  # 自定义值
        self.reverse = reverse  # 自定义值
        self.related_field_list = related_field_list  # 自定义值
        self.queryset = queryset  # 自定义值
        self.limit_num = limit_num  # 自定义值

    def get_field_value(self, obj=None):
        """获取字段的值"""
        field_value = None
        res = {}
        if obj is not None:
            if self.model_func:
                field_value = getattr(obj, self.model_func.__name__)()
            else:
                field_value = getattr(obj, self.name, None)  # 这里 getattr 时必须使用self.name
            if field_value:
                if self.datetime_format:
                    field_value = field_value.strftime(self.datetime_format.value)
                if self.model_field and self.model_field.field.choices:
                    field_value_display = getattr(obj, 'get_%s_display' % self.name)()
                    res[f"{self.out_name}_display"] = field_value_display
        res[self.out_name] = field_value
        return res

    def __str__(self):
        return self.name

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        return f"""{start_str}"{self.out_name}": {self.label}{',' if not is_last else ''}"""


class ValueField(BaseReturnField):

    def get_field_value(self, obj=None):
        return {
            self.out_name: self.value
        }


class AnnotateField(BaseReturnField):
    pass


class ModelField(BaseReturnField):
    pass


class ModelFuncField(ModelField):
    pass


class ModelRelatedField(ModelField):

    def get_related_list(self, parent_field_name="", is_prefetch=False):
        related_name = f"{parent_field_name}__{self.name}" if parent_field_name else self.name
        data_list = []
        child_data_list = []
        field_list = []
        if self.reverse:
            if isinstance(self.model_field.field, RelatedForeignKey):
                # 去掉会产生额外的数据库查询
                field_list.append(f"{self.model_field.field.name}_id")
        annotate_res = {}
        for field in self.related_field_list:
            if isinstance(field, ForeignKeyField):
                if self.reverse:
                    # 去掉会产生额外的数据库查询
                    field_list.append(f"{field.name}_id")
                child_data_list.extend(field.get_related_list(related_name, is_prefetch=is_prefetch))
            elif isinstance(field, ManyToManyField):
                child_data_list.extend(field.get_related_list(related_name, is_prefetch=True))
            elif isinstance(field, ModelField):
                field_list.append(field.out_name)
            elif isinstance(field, AnnotateField):
                annotate_res[field.out_name] = field.annotate_func(self)
            else:
                continue
        if is_prefetch:
            if self.queryset is None:
                queryset = self.model_field.field.related_model.objects.active()
            else:
                queryset = self.queryset
            if annotate_res:
                queryset = queryset.annotate(**annotate_res)
            data_list.append(
                Prefetch(
                    related_name,
                    queryset=queryset.only(*field_list),
                ),
            )
        else:
            data_list.append(related_name)
        data_list.extend(child_data_list)
        return data_list


class ForeignKeyField(ModelRelatedField):

    def get_field_value(self, obj=None):
        """获取字段的值"""
        field_value = None
        res = {}
        if obj is not None:
            related_obj = getattr(obj, self.name, None)
            if related_obj is not None:
                field_value = {"id": related_obj.id}
                for field in self.related_field_list:
                    field_value.update(field.get_field_value(related_obj))

        res[self.out_name] = field_value
        return res

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        t_count += 1
        field_str_list = []
        for inx, field in enumerate(self.related_field_list):
            field_str_list.append(f"{field.get_showdoc_str(t_count, is_last=inx == len(self.related_field_list) - 1)}")
        field_list_str = "\n".join(field_str_list)
        ss = f"""{start_str}"{self.out_name}": {{ {self.label},
{field_list_str}
{start_str}}}{',' if not is_last else ''}"""
        return ss


class ManyToManyField(ModelRelatedField):

    def get_field_value(self, obj=None):
        """获取字段的值"""
        field_value = None
        res = {}
        if obj is not None:
            field_value = []
            related_obj_list = getattr(obj, self.name).all()
            if self.limit_num is not None:
                related_obj_list = related_obj_list[:self.limit_num]
            for related_obj in related_obj_list:
                related_value = {"id": related_obj.id}
                for field in self.related_field_list:
                    related_value.update(field.get_field_value(related_obj))
                field_value.append(related_value)
        res[self.out_name] = field_value
        return res

    def get_showdoc_str(self, t_count=1, is_last=False):
        start_str = "".join(["\t"] * t_count)
        t_count += 1
        field_start_str = "".join(["\t"] * t_count)
        t_count += 1
        field_str_list = []
        for inx, field in enumerate(self.related_field_list):
            field_str_list.append(f"{field.get_showdoc_str(t_count, is_last=inx == len(self.related_field_list) - 1)}")
        field_list_str = "\n".join(field_str_list)
        ss = f"""{start_str}"{self.out_name}": [ {self.label}
{field_start_str}{{
{field_list_str}
{field_start_str}}}
{start_str}]{',' if not is_last else ''}"""
        return ss
