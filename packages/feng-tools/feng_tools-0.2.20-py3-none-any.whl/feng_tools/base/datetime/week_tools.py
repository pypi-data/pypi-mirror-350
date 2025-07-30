# 定义中文星期的映射
from datetime import date

weekday_map = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期日'
}

def get_date_week(date_value:date):
    """获取日期的星期几"""
    return weekday_map[date_value.weekday()]



if __name__ == '__main__':
    current_date = date(year=2025, month=4, day=28)
    print(get_date_week(current_date)) # 星期一