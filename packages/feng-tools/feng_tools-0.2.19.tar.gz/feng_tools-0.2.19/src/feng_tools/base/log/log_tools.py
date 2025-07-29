"""
日志通用工具
"""
import traceback


def get_error_msg(error_msg: str, exc: Exception = None):
    """
    获取错误信息（通常用于包含异常信息的输出）
    """
    if exc:
        return f'{error_msg}:{exc}\n {traceback.format_exc()}'
    else:
        return f'{error_msg}\n {traceback.format_exc()}'