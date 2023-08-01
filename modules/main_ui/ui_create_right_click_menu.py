import logging
import traceback
from typing import Union

import ttkbootstrap as ttk

from modules.configs import LANG

logger = logging.getLogger(__name__)


def ui_create_right_click_menu(widget: Union[ttk.Entry, ttk.Text]) -> None:
    """
    创建一个右键弹出菜单，并绑定到指定的 widget。

    :param widget: 需要绑定右键菜单的控件，可以是 ttk.Entry 或 ttk.Text 类型。
    :type widget: Union[ttk.Entry, ttk.Text]
    :rtype: None
    """

    # noinspection PyShadowingNames
    def create_menu(event) -> None:
        """创建右键菜单并显示。"""
        try:
            right_click_menu = ttk.Menu(tearoff=1, takefocus=0)
            right_click_menu.add_command(label=LANG["RM_cut"], command=lambda: widget.event_generate('<<Cut>>'))
            right_click_menu.add_command(label=LANG["RM_copy"], command=lambda: widget.event_generate('<<Copy>>'))
            right_click_menu.add_command(label=LANG["RM_paste"], command=lambda: widget.event_generate('<<Paste>>'))
            right_click_menu.add_separator()
            right_click_menu.add_command(label=LANG["RM_select_all"], command=lambda: widget.event_generate('<<SelectAll>>'))
            right_click_menu.add_command(label=LANG["RM_delete"], command=lambda: widget.event_generate('<<Clear>>'))

            if isinstance(widget, ttk.Text):
                right_click_menu.add_command(label=LANG["RM_undo"], command=lambda: widget.event_generate('<<Undo>>'))
                right_click_menu.add_command(label=LANG["RM_redo"], command=lambda: widget.event_generate('<<Redo>>'))
            right_click_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            logger.error(f"An error occurred while creating the right click menu: {e}\n{traceback.format_exc()}")

    try:
        widget.bind("<Button-3>", create_menu)
    except Exception as e:
        logger.error(f"An error occurred while binding the right click menu: {e}\n{traceback.format_exc()}")
