from enum import Enum


class RePatternEnum(Enum):
    """常见正则表达式枚举"""
    # 邮箱地址的正则表达式
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # 中国大陆手机号码的正则表达式
    phone_pattern = r'1[3-9]\d{9}'
    # 国际手机号码的正则表达式
    phone_international_pattern = r'\+?[1-9]\d{1,14}'
    # 中国大陆身份证号码（15位或18位）
    id_card_pattern = r'\d{15}(\d{2}[0-9Xx])?'
    # 中国大陆邮政编码
    zip_code_pattern = r'\d{6}'
    # 美国邮政编码
    zip_code_us_pattern = r'\d{5}(-\d{4})?'
    # 时间 HH:MM
    time_s_pattern = r'([01]\d|2[0-3]):([0-5]\d)'
    # 时间 HH:MM:SS
    time_pattern = r'([01]\d|2[0-3]):([0-5]\d):([0-5]\d)'
    # 日期 YYYY-MM-DD
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    # 日期 DD/MM/YYYY
    date_international_pattern = r'\d{2}/\d{2}/\d{4}'
    # 匹配日期时间 YYYY-MM-DD HH:MM:SS
    datetime_pattern = r'\d{4}-\d{2}-\d{2} ([01]\d|2[0-3]):([0-5]\d):([0-5]\d)'
    # IPv4
    ipv4_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    # IPv6
    ipv6_pattern = r'(([0-9a-fA-F]{1,4}):){7}([0-9a-fA-F]{1,4})'
    # 标准UUID
    uuid_pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
    # 基本URL模式
    url_pattern = r'(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(:[0-9]+)?(/.*)?'
    # 匹配所有HTML标签
    html_tag_pattern = r'<[^>]+>'
    # 匹配所有特殊字符
    special_char_pattern = r'[^\w\s]'

