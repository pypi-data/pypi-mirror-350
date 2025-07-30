"""
系统相关工具
"""
import platform


def get_system_bit() -> str:
    """
    获取当前安装版本为x86还是x64
    :return: x64、x86
    """
    architecture_data = platform.architecture()
    if architecture_data[0] == "32bit":
        return "x86"
    # architecture_data[0] == "64bit"
    return "x64"


def get_system() -> str:
    """
    获取系统信息
    :return: linux、windows、mac
    """
    system_data = platform.system()
    if system_data == 'Linux':
        return 'linux'
    elif system_data == 'Windows':
        return 'windows'
    elif system_data == 'Darwin':
        return 'mac'
    else:
        raise NotImplementedError


if __name__ == '__main__':
    print(get_system())
    print(get_system_bit())