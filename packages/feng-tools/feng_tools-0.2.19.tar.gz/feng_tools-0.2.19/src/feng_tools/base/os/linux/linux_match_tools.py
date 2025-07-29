"""
Linux通配符匹配工具类
"""
import fnmatch


def match_any(string: str, pattern_list: list) -> bool:
    """
    是否匹配linux通配符列表中的任一规则
    :param string: 要进行匹配的内容
    :param pattern_list: linux通配符列表
    :return: True/False
    """
    for pattern in pattern_list:
        if fnmatch.fnmatch(string, pattern):
            return True
    return False


def match_all(string: str, pattern_list: list) -> bool:
    """
    是否匹配linux通配符列表中的所有规则
    :param string: 要进行匹配的内容
    :param pattern_list: linux通配符列表
    :return: True/False
    """
    for pattern in pattern_list:
        if not fnmatch.fnmatch(string, pattern):
            return False
    return True
