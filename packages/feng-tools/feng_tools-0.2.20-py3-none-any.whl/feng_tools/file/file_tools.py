import os
import traceback
from typing import Union, Generator


def read_file(data_file:str, binary_flag: bool = False) -> Union[str, bytes]:
    """
    读取文件字符串
    :param data_file: 数据文件
    :param binary_flag: 是否是二进制文件，如果True,则按照二进制读取
    :return: None或文件内容
    """
    if os.path.exists(data_file) and os.path.isfile(data_file):
        try:
            mode = 'rb' if binary_flag else 'r'
            encoding = None if binary_flag else 'utf-8'
            with open(data_file, mode, encoding=encoding) as f:
                return f.read()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"读取文件失败: {str(e)}")
    else:
        raise ValueError(f"文件不存在: {data_file}")


def read_file_by_iterate(data_file: str, binary_flag=False, buffer_size=50 * 1024):
    """
    迭代读取文件字符串（当文件较大时，可以使用）
    :param data_file: 数据文件
    :param binary_flag: 是否是二进制文件，如果True,则按照二进制读取
    :param buffer_size: 缓存区大小
    :return: 文件内容
    """
    if os.path.exists(data_file) and os.path.isfile(data_file):
        mode = 'rb' if binary_flag else 'r'
        encoding = None if binary_flag else 'utf-8'
        with open(data_file, mode, encoding=encoding) as f:
            # 读取buffer_size字节的数据
            data = f.read(buffer_size)
            while data:
                # 处理数据
                yield data
                # 继续读取下一个buffer_size字节的数据
                data = f.read(buffer_size)
    else:
        raise ValueError(f"文件不存在: {data_file}")

# def read_files(file_dir: str, file_name_pattern: str) -> dict[str, str]:
#     """
#     批量读取某些文件的内容
#     :param file_dir: 文件目录
#     :param file_name_pattern: 文件名规则， 如: *.css
#     :return: {'文件名':'文件内容'}
#     """
#     tmp_file_list = get_file_list(file_path, file_pattern)
#     tmp_file_list = filename_sort(tmp_file_list)
#     file_info_dict = {}
#     for tmp_file in tmp_file_list:
#         file_info_dict[os.path.split(tmp_file)[1]] = read_file(tmp_file)

def save_file(file_data: str | bytes, save_data_file: str) -> str:
    """
    保存文件
    :param file_data: 文件内容
    :param save_data_file: 保存内容的文件
    :return: 保存的文件
    """
    # 是否是二进制文件，如果True,则按照二进制写入
    binary_flag = isinstance(file_data, bytes)
    mode = 'wb' if binary_flag else 'w'
    encoding = None if binary_flag else 'utf-8'
    os.makedirs(os.path.dirname(save_data_file), exist_ok=True)
    with open(save_data_file, mode, encoding=encoding) as f:
        f.write(file_data)
    return save_data_file



def save_html_file(file_data: str | bytes, save_data_file: str,  append_jinja2_raw=False):
    """
    保存html文件
    :param file_data: 文件内容
    :param save_data_file: 保存的html文件
    :param append_jinja2_raw: 添加jinja2的{% raw %}， 用于确保模板中的某些内容不会被错误地转义
    :return: 保存的html文件
    """
    # 确保文件内容不为空
    if not file_data:
        raise ValueError("文件内容为空，无法保存")
    binary_flag = isinstance(file_data, bytes)
    mode = 'wb' if binary_flag else 'w'
    encoding = None if binary_flag else 'utf-8'
    if append_jinja2_raw:
        if binary_flag:
            file_data = '{% raw %}'.encode('utf-8') + file_data + '{% endraw %}'.encode('utf-8')
        else:
            file_data = '{% raw %}' + file_data + '{% endraw %}'
    os.makedirs(os.path.dirname(save_data_file), exist_ok=True)
    with open(save_data_file, mode, encoding=encoding) as f:
        f.write(file_data)
    return save_data_file

def append_file(file_data: str | bytes, save_data_file: str) -> str:
    """
    追加文件
    :param file_data: 文件内容
    :param save_data_file: 保存内容的文件
    :return: 保存的文件
    """
    # 如果是字节，就按照二进制形式追加
    binary_flag = isinstance(file_data, bytes)
    mode = 'ab' if binary_flag else 'a'
    encoding = None if binary_flag else 'utf-8'
    os.makedirs(os.path.dirname(save_data_file), exist_ok=True)
    with open(save_data_file, mode, encoding=encoding) as f:
        f.write(file_data)
    return save_data_file



