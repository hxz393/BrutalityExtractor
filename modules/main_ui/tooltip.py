from typing import Optional

import ttkbootstrap as ttk


# noinspection PyUnusedLocal,PyArgumentList
class ToolTip:
    def __init__(self, widget: ttk.widgets, text: str, switch: ttk.Variable) -> None:
        """
        初始化 ToolTip 对象。

        :param widget: tkinter 控件。
        :type widget: ttk.Widget
        :param text: ToolTip 中显示的文本。
        :type text: str
        :param switch: 控制是否显示 ToolTip 的变量。
        :type switch: ttk.Variable
        """
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.switch = switch
        self.switch.trace_add('write', self.update_tooltip_status)

        # 根据初始状态绑定事件
        if not self.switch.get():
            self.bind_tooltip()

    def bind_tooltip(self) -> None:
        """绑定鼠标进入和离开事件，用于显示和隐藏 ToolTip。"""
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def unbind_tooltip(self) -> None:
        """解绑鼠标进入和离开事件。"""
        self.widget.unbind("<Enter>")
        self.widget.unbind("<Leave>")

    def show_tooltip(self, event: Optional[str] = None) -> None:
        """
        显示 ToolTip。

        :param event: 事件对象，默认为 None。
        :type event: Optional[str]
        """
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 35
        y += self.widget.winfo_rooty() + 35

        self.tooltip_window = ttk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        ttk.Label(self.tooltip_window, bootstyle='inverse-light', text=self.text, relief="solid", borderwidth=1, padding=(5, 1)).pack()

    def hide_tooltip(self, event: Optional[str] = None) -> None:
        """
        隐藏 ToolTip。

        :param event: 事件对象，默认为 None。
        :type event: Optional[str]
        """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_tooltip_status(self, *args) -> None:
        """更新 ToolTip 的状态，即根据 switch 变量的值决定是否显示 ToolTip。"""
        if self.switch.get():
            self.unbind_tooltip()
        else:
            self.bind_tooltip()
