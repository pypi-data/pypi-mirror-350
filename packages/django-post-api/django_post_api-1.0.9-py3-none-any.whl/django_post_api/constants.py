from .enums import BaseEnum


class DateTimeFormatEnum(BaseEnum):
    day = "%Y-%m-%d"
    time = "%H:%M:%S"
    day_minute = "%Y-%m-%d %H:%M"
    day_time = "%Y-%m-%d %H:%M:%S"


class QueryWayEnum(BaseEnum):
    same = ""
    icontains = "__icontains"
    include = "__in"
    gt = "__gt"
    gte = "__gte"
    lt = "__lt"
    lte = "__lte"


class ParamNameEnum(BaseEnum):
    obj_params = "obj_params"
    obj_many_to_many_params = "obj_many_to_many_params"
    obj_related_many_to_many_params = "obj_related_many_to_many_params"
