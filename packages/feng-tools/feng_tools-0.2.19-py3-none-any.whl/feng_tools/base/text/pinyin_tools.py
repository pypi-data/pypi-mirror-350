"""
拼音工具类
pip install pypinyin
"""
from pypinyin import pinyin, lazy_pinyin, Style

def get_pinyin_with_tone(chinese_text)->list[list[str]]:
    """
    获取带声调的拼音
    :param chinese_text: 中文字符串 示例输入：中文
    :return: 二维列表形式的拼音 示例输出: [['zhōng'], ['wén']]
    """
    return pinyin(chinese_text)

def get_lazy_pinyin_without_tone(chinese_text)->list[str]:
    """
    获取不带声调的拼音
    :param chinese_text: 中文字符串 示例输入：中文
    :return: 列表形式的拼音  示例输出: ['zhong', 'wen']
    """
    return lazy_pinyin(chinese_text)

def get_first_letter(chinese_text)->list[str]:
    """
    获取首字母
    :param chinese_text: 中文字符串 示例输入：中文
    :return: 列表形式的首字母  示例输出: ['z', 'w']
    """
    return lazy_pinyin(chinese_text, style=Style.FIRST_LETTER)

def get_lazy_pinyin_with_digit_tone(chinese_text)->list[str]:
    """
    获取带数字声调的拼音
    :param chinese_text: 中文字符串  示例输入：中文
    :return: 列表形式的带数字声调的拼音  示例输出: ['zho1ng', 'we2n']
    """
    return lazy_pinyin(chinese_text, style=Style.TONE2)


if __name__ == '__main__':
    text = "中文"
    print(get_pinyin_with_tone(text))  # 输出: [['zhōng'], ['wén']]
    print(get_lazy_pinyin_without_tone(text))  # 输出: ['zhong', 'wen']
    print(get_first_letter(text))  # 输出: ['z', 'w']
    print(get_lazy_pinyin_with_digit_tone(text))  # 输出: ['zho1ng', 'we2n']
