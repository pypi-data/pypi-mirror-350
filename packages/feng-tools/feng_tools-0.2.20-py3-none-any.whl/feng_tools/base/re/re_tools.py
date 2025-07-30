import re
from typing import List, AnyStr, Any

from feng_tools.base.re import RePatternEnum


def high_light_word(content_text: str, keyword: str, high_light_tag: str = 'em') -> str:
    """
    单词高亮
    """
    if content_text:
        re_pattern = f'({re.escape(keyword)})'
        if re.search(re_pattern, content_text, flags=re.RegexFlag.I):
            return re.sub(re_pattern, f'<{high_light_tag}>\\1</{high_light_tag}>', content_text, flags=re.RegexFlag.I)
    return content_text


def get_match_groups(pattern:str, content:str) -> tuple[str | Any, ...] | None:
    """
    获取规则匹配的分组内容
    :param pattern: 正则表达式
    :param content: 内容
    :return: tuple或None 匹配的分组内容
    """
    re_match = re.compile(pattern, re.S).search(content)
    if re_match:
        return re_match.groups()
    return None


def get_match_first_group(pattern:str, content:str) -> AnyStr | None | Any:
    """
    获取规则匹配的第一个分组内容
    :param pattern: 正则表达式
    :param content: 内容
    :return: 匹配的第一个分组内容
    """
    re_match_tuple = get_match_groups(pattern, content)
    if re_match_tuple:
        return re_match_tuple[0]
    return None


def match(text, pattern):
    return re.match(pattern, text)

def match_email(text):
    """
    匹配邮箱
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.email_pattern.value}$')

def match_phone(text):
    """
    匹配手机号
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.phone_pattern.value}$')

def match_date(text):
    """
    匹配日期
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.date_pattern.value}$')

def match_time(text):
    """
    匹配时间
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.time_pattern.value}$')

def match_datetime(text):
    """
    匹配日期时间
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.datetime_pattern.value}$')

def match_ip(text):
    """
    匹配ip
    :param text:
    :return:"""
    return match(text, f'^{RePatternEnum.ipv4_pattern.value}$')


def high_light_word(content_text: str, keyword: str, high_light_tag: str = 'em') -> str:
    """
    高亮显示关键字
    :param content_text: 文本内容
    :param keyword: 关键字
    :param high_light_tag: 高亮标签
    :return: 高亮显示后的文本
    """
    if content_text:
        re_pattern = f'({re.escape(keyword)})'
        if re.search(re_pattern, content_text, flags=re.RegexFlag.I):
            return re.sub(re_pattern, f'<{high_light_tag}>\\1</{high_light_tag}>', content_text, flags=re.RegexFlag.I)
    return content_text


def search(text, pattern) -> List[str]:
    """
    搜索文本
    :param text:
    :param pattern:
    :return:
    """
    if not text or not pattern:
        return []
    re_compile = re.compile(pattern, re.S)
    re_search_result = re_compile.findall(text)
    return re_search_result


def escape(str_text:str):
    """将字符串转为正则的pattern"""
    return re.escape(str_text)


if __name__ == '__main__':
    emails = ["example@example.com", "invalid-email", "user@domain.co"]
    for email in emails:
        print(match_email(email))

    test_text= '陈铁锋手机: 13812345678, 王五邮箱: example@example.com, 张三手机: 13812345678'
    print(search(test_text, RePatternEnum.phone_pattern.value))
    print(search(test_text, RePatternEnum.email_pattern.value))

    wx_pattern = r'<ToUserName><!\[CDATA\[(.*?)\]\]></ToUserName>'
    content = '<ToUserName><![CDATA[toUser]]></ToUserName>'
    print(search(content, pattern))