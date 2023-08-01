import logging
import traceback
import tkinter as tk

from ttkbootstrap.dialogs import Messagebox

from modules.configs import LANG

logger = logging.getLogger(__name__)


def ui_display_msg(root: tk.Tk, message: str, level: str) -> None:
    """
    在 tkinter UI 中显示指定级别的信息。

    :param root: tkinter 的 root 对象
    :type root: tk.Tk
    :param message: 要显示的消息文本
    :type message: str
    :param level: 消息的级别，可以是 'info'、'warning' 或 'error'
    :type level: str
    :return: 无返回值
    """
    try:
        if level not in ['info', 'warning', 'error']:
            raise ValueError("The level must be one of the following: 'info', 'warning', 'error'")

        if level == 'info':
            root.after(10, lambda: Messagebox.show_info(title=LANG["msg_info_title"], message=message))
        elif level == 'warning':
            root.after(10, lambda: Messagebox.show_warning(title=LANG["msg_warning_title"], message=message))
        elif level == 'error':
            root.after(10, lambda: Messagebox.show_error(title=LANG["msg_error_title"], message=message))
    except Exception as e:
        logger.error(f"An error occurred while displaying the message: {e}\n{traceback.format_exc()}")
        return None
