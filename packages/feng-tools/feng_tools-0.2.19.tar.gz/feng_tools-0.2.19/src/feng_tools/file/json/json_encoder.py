import datetime

import json
from array import array
from enum import Enum
from pydantic.json import pydantic_encoder
from _decimal import Decimal

from feng_tools.common.enums import EnumItem


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, array):
            return obj.tolist()
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, Enum):
            if isinstance(obj.value, str | int | float):
                return obj.value
            elif isinstance(obj.value, EnumItem):
                if obj.value.value is not None:
                    return obj.value.value
            return obj.name

        else:
            return super(JsonEncoder, self).default(obj)

