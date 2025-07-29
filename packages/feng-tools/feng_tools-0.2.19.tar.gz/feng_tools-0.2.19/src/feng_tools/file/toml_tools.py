"""
Python 3.11 及以上版本内置了 tomllib 模块，可直接解析 TOML 文件。
Python 3.11 以下版本需要安装第三方库 tomli。
"""
import tomllib
from typing import Any, Dict


def read_toml(file_path: str) -> Dict[str, Any]:
    """
    读取并返回 TOML 文件的内容。
    Args:
        file_path (str): TOML 文件的路径。
    Returns:
        dict: 包含 TOML 文件内容的字典。
    Raises:
        FileNotFoundError: 如果指定的文件路径不存在。
        tomllib.TOMLDecodeError: 如果 TOML 文件格式不正确。
    """
    with open(file_path, "rb") as f:
        return tomllib.load(f)
