from datetime import time


def parse_time(time_str:str) -> time:
    """HH:MM字符串转time对象"""
    h,m=map(int, time_str.split(':'))
    return time(hour=h, minute=m)

