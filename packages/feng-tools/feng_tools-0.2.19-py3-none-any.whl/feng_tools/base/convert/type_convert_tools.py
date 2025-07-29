"""
类型转换工具
"""
from array import array
from datetime import datetime, date, time
from enum import Enum
from typing import Any, Type

from _decimal import Decimal

from feng_tools.common.enums import EnumItem


def convert_value_to_type(value: Any, to_type: Type[Any],
                          datetime_format: str = '%Y-%m-%d %H:%M:%S',
                          date_format: str = '%Y-%m-%d',
                          time_format: str = '%H:%M:%S') -> Any:
    """
    转换值为某个类型
    :param value: 原值
    :param to_type: 需要的类型
    :param datetime_format: 日期时间格式
    :param date_format: 日期格式
    :param time_format:时间格式
    :return: 转换后的值
    """
    if to_type.__name__ == 'Optional':
        to_type = to_type.__dict__.get('__args__')[0]
    if to_type is None:
        return value
    elif isinstance(value, str):
        value = value.strip()
    if isinstance(value, str) and len(value) == 0:
        return None
    if isinstance(value, to_type):
        return value
    elif isinstance(value, datetime) and issubclass(to_type, str):
        return value.strftime(datetime_format)
    elif isinstance(value, str) and issubclass(datetime, to_type):
        return datetime.strptime(value, datetime_format)
    elif isinstance(value, str) and issubclass(date, to_type):
        return datetime.strptime(value, date_format)
    elif isinstance(value, str) and issubclass(time, to_type):
        return datetime.strptime(value, time_format)
    elif issubclass(str, to_type):
        return str(value)
    elif issubclass(int, to_type):
        return int(value)
    elif issubclass(float, to_type):
        return float(value)
    elif issubclass(bool, to_type) and isinstance(value, str):
        return 'true' == value.lower() or '1' == value
    elif isinstance(value, date) and issubclass(to_type, str):
        return value.strftime(date_format)
    elif isinstance(value, time) and issubclass(to_type, str):
        return value.strftime(time_format)
    elif isinstance(value, bytes) and issubclass(to_type, str):
        return str(value, encoding='utf-8')
    elif isinstance(value, array):
        return value.tolist()
    elif isinstance(value, Decimal) and issubclass(to_type, str):
        return str(value)
    elif isinstance(value, Enum) and not issubclass(to_type, Enum):
        if isinstance(value.value, str):
            return value.value
        elif isinstance(value.value, EnumItem) and value.value.value:
            return value.value.value
        return value.name
    elif not isinstance(value, Enum) and issubclass(to_type, Enum):
        enum_list = [tmp for tmp in to_type if tmp.name == value or tmp.value == value or tmp.value.value == value]
        if enum_list:
            return enum_list[0]
        else:
            return value
    else:
        return str(value)
