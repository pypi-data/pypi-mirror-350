"""
操作系统相关工具
"""
import os


def get_user_home() -> str:
    """获取用户目录"""
    return os.path.expanduser('~')


if __name__ == '__main__':
    print(get_user_home())