"""
pip install python-dateutil
"""
import datetime

from dateutil import parser

def parse_time(time_str:str) -> datetime.time:
    """
    转换时间
    :params time_str: 如：15:30:02
    """
    return parser.parse(time_str)

def parse_date(date_str:str) -> datetime.date:
    """
    转换日期
    :params date_str: 如：2025-05-01
    """
    return parser.parse(date_str)

def parse_datetime(datetime_str:str) -> datetime.datetime:
    """
    转换日期时间
    :params datetime_str: 如：2025-05-01 15:30:02、2025-05-01 15:30:02+08:00
    """
    return parser.parse(datetime_str)

def parse_(datetime_str:str) -> datetime.datetime|datetime.date|datetime.time:
    """
        转换日期时间
        :params datetime_str: 如：2025-05-01 15:30:02、2025-05-01、15:30:02
        """
    return parser.parse(datetime_str)
