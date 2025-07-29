from enum import Enum
from typing import Literal


class BaseEnum(Enum):
    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj._data_ = args
        obj._value_ = args[0]
        return obj

    @property
    def data(self):
        return self._data_

    @classmethod
    def get_param_choice_list(cls):
        return cls.get_choice_list("name", "value", "param")

    @classmethod
    def get_mysql_choice_list(cls):
        return cls.get_choice_list("name", "value", "mysql")

    def get_value_by_param(self, param):
        if hasattr(self, param):
            return getattr(self, param)
        elif param.startswith("data[") and param.endswith("]"):
            index = int(param[5:-1])  # 提取索引值
            return self.data[index]
        else:
            raise ValueError(f"Invalid value: {param}")

    @classmethod
    def get_choice_list(cls, key_name, label_name, return_format: Literal["mysql", "param"] = "param",
                        member_list=None):
        data_list = []
        for member in cls:
            if member_list is not None and member not in member_list:
                continue
            key_value = member.get_value_by_param(key_name)
            label_value = member.get_value_by_param(label_name)
            if return_format == "mysql":
                data_list.append((key_value, label_value))
            elif return_format == "param":
                data_list.append({"value": key_value, "label": label_value})
            else:
                raise ValueError(f"Invalid value: {return_format}")
        return data_list

    @classmethod
    def get_member_by_value(cls, value):
        """
        根据值查询枚举成员。
        如果找不到，返回 None。
        """
        for member in cls:
            if member.value == value:
                return member
        return None
