"""
消息通知工具： pip install win10toast -i https://pypi.tuna.tsinghua.edu.cn/simple/ -U
"""
from win10toast import ToastNotifier


def notify(title, message, duration: int = 10, icon_file:str=None) -> None:
    """
    windows通知提醒
    :param title: 标题
    :param message: 内容
    :param duration: 持续时间，默认10秒、
    :param icon_file: 图标
    :return: None
    """
    if not icon_file:
        icon_file = r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.17.11461.0_x64__8wekyb3d8bbwe\Images\terminal_contrast-white.ico"
    toast = ToastNotifier()
    toast.show_toast(title=title, msg=message, icon_path=icon_file, duration=duration)


if __name__ == '__main__':
    notify('测试', '这是一个测试通知')