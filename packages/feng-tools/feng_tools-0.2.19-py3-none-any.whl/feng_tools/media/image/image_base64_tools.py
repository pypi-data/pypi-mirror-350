"""
图片和base64工具
"""
import base64
import re

from feng_tools.web.http import http_mimetype_tools


def base64_to_image(img_base64_data: str, save_image_file: str) -> str:
    """
    base64图片数据转换为图片
    :param img_base64_data: base64图片数据
    :param save_image_file: 保存的图片文件，如：output/tests.png
    :return: save_image 保存的图片文件
    """
    img_data = base64.b64decode(re.sub('^data:image/.+;base64,', '', img_base64_data))
    with open(save_image_file, mode='wb') as file:
        file.write(img_data)
    return save_image_file


def image_to_base64(image_file: str) -> str:
    """
    图片转为base64
    :param image_file: 图片文件
    :return: base64图片字符串
    """
    with open(image_file, 'rb') as file:
        image_data = file.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
    mimetype = http_mimetype_tools.get_mimetype(image_file)
    return f'data:{mimetype[0]};base64,{base64_data}'

