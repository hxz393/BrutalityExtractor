from tkinter import EW, LEFT, BOTH, RIGHT, NSEW
import logging
from typing import Optional

import ttkbootstrap as ttk
from tkfontawesome import icon_to_image
from ttkbootstrap import PRIMARY, Bootstyle, INVERSE

from modules import ICO_SIZE, FONT_SIZE, mini_skin_config

logger = logging.getLogger(__name__)


class CollapsingFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        """
        初始化 CollapsingFrame 对象。

        :param master: 父 Frame。
        """
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.img_down = icon_to_image("angle-double-down", fill="#FFFFFF", scale_to_height=ICO_SIZE)
        self.img_up = icon_to_image("angle-double-up", fill="#FFFFFF", scale_to_height=ICO_SIZE)

    def add(self, child, title: str = "", bootstyle: str = PRIMARY, image: str = '', display: int = 0, **kwargs) -> None:
        """
        向 Frame 中添加子组件。

        :type child: ttk.Frame
        :param child: 要添加的子 Frame。
        :type title: str
        :param title: 子 Frame 的标题。
        :type bootstyle: str
        :param bootstyle: 子 Frame 的样式。
        :type image: str
        :param image: 子 Frame 的图像。
        :type display: int
        :param display: 子 Frame 是否可见。
        """
        try:
            if child.winfo_class() != 'TFrame':
                logger.error('The child class should be TFrame')
                return

            style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
            frm = ttk.Frame(self, bootstyle=style_color)
            frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

            image_label = ttk.Label(
                master=frm,
                bootstyle=(style_color, INVERSE),
                compound=LEFT,
                image=image
            )
            image_label.pack(side=LEFT, padx=10)

            header = ttk.Label(
                master=frm,
                text=title,
                bootstyle=(style_color, INVERSE),
                font=('', FONT_SIZE),
            )
            header.pack(side=LEFT, fill=BOTH)

            if kwargs.get('textvariable'):
                header.configure(textvariable=kwargs.get('textvariable'))

            def _func(c=child):
                return self._toggle_open_close(c)

            btn = ttk.Button(
                master=frm,
                image=self.img_down,
                bootstyle=style_color,
                command=_func
            )
            btn.pack(side=RIGHT)

            child.btn = btn
            child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

            self.cumulative_rows += 2

            if not display:
                btn['image'] = self.img_up
                child.grid_remove()
        except Exception as e:
            logger.error(f"An error occurred while adding the child to the frame: {e}")

    def _toggle_open_close(self, child):
        """
        切换子 Frame 的开启或关闭状态。

        :type child: ttk.Frame
        :param child: 要切换状态的子 Frame。
        """
        try:
            if child.winfo_viewable():
                child.grid_remove()
                child.btn.configure(image=self.img_up)
            else:
                child.grid()
                child.btn.configure(image=self.img_down)

            self.update_size()
        except Exception as e:
            logger.error(f"An error occurred while toggling the status of the child frame: {e}")

    def update_size(self) -> None:
        """
        更新 Frame 的尺寸。
        """
        try:
            self.update_idletasks()
            plug_height = 30 if mini_skin_config else 62
            new_height = sum(c.winfo_height() for c in self.grid_slaves()) + plug_height
            self.master.geometry(f"{self.master.winfo_width()}x{new_height}")
        except Exception as e:
            logger.error(f"An error occurred while updating the frame size: {e}")

