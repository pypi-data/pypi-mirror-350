"""
系统相关工具
"""
import re
import winreg


def get_desktop_path():
    """获取桌面路径"""
    _key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(_key, "Desktop")[0]


def del_special_symbol(s: str) -> str:
    """删除Windows文件名中不允许的字符"""
    return re.sub(r'[:*?"<>|]', '_', s)

