"""
pillow: pip install pillow  -i https://pypi.tuna.tsinghua.edu.cn/simple/ -U
"""
from PIL import Image


def show_image(image_file: str, title: str = None):
    """
    显示图片
    :param image_file: 图片文件
    :param title: 标题
    :return: pil_image
    """
    pil_image = Image.open(image_file)
    pil_image.show(title=title)
    return pil_image


