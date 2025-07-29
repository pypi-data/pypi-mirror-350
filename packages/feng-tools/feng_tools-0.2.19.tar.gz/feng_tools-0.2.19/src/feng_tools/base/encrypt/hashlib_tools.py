"""
hashlib加密工具
"""
import hashlib
import hmac
import os


def calc_unique_id(data_list: list, split_chat: str = '') -> str:
    """
    计算唯一id
    :param data_list: 字符串列表
    :param split_chat: 分割符
    :return:
    """
    data_list = [str(tmp) for tmp in filter(lambda x: x is not None, data_list)]
    return calc_md5(split_chat.join(data_list))


def calc_byte_md5(data_byte: bytes) -> str:
    """计算md5"""
    return hashlib.md5(data_byte).hexdigest()


def calc_md5(data_str: str) -> str:
    """计算md5"""
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()


def calc_file_md5(data_file: str, is_lower: bool = True) -> str:
    """计算文件的md5"""
    with open(data_file, 'rb') as f:
        if is_lower:
            return hashlib.md5(f.read()).hexdigest().lower()
        else:
            return hashlib.md5(f.read()).hexdigest()


def calc_file_slice_md5(data_file: str, slice_length: int = 256 * 1024) -> str:
    """文件校验段的MD5，32位小写，校验段对应文件前256KB"""
    if os.path.getsize(data_file) >= slice_length:
        with open(data_file, 'rb') as f:
            return hashlib.md5(f.read(slice_length)).hexdigest()
    else:
        return calc_file_md5(data_file=data_file)


def calc_hmac_sha512(secret_key: str, data: str) -> str:
    """
    计算sha512值
    :param secret_key: 加密的键
    :param data: 要加密的数据
    :return: sha512值
    """
    hash_func = hashlib.sha512
    return hmac.new(key=secret_key.encode('utf-8'),
                    msg=data.encode('utf-8'),
                    digestmod=hash_func).hexdigest()


def calc_sha1(data_str: str) -> str:
    """
    计算sha1值
    :param data_str: 要加密的数据
    :return: sha512值
    """
    return hashlib.sha1(data_str.encode('utf-8')).hexdigest()


def calc_file_sha1(data_file: str) -> str:
    """
    计算sha1值
    :param data_file: 要加密的文件
    :return: sha512值
    """
    with open(data_file, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()


def calc_sha224(data_str: str) -> str:
    """
    计算sha1值
    :param data_str: 要加密的数据
    :return: sha512值
    """
    return hashlib.sha224(data_str.encode('utf-8')).hexdigest()


def calc_sha512(data_str: str) -> str:
    """
    计算sha512值
    :param data_str: 要加密的数据
    :return: sha512值
    """
    return hashlib.sha512(data_str.encode('utf-8')).hexdigest()
