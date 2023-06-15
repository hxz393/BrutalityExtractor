import webbrowser
import time
import os.path
import requests
import urllib3
from multiprocessing import Pool, freeze_support, cpu_count
from threading import Thread
import psutil
from functools import partial

import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.style import Bootstyle
from tkinter import filedialog
from tkfontawesome import icon_to_image

from modules.log_conf import configure_logging
from modules.file_unzip import unzip
from modules.file_ops import *
from modules.math_until import *
from modules.conf_init import *

logger = configure_logging(console_output=True, log_file = "logs/run.log", log_level=log_level_config, max_log_size=log_size_config, backup_count=log_count_config)


def thread_it(func, *args, daemon=True, name=None):
    """
    多线程运行

    :param func: 函数名
    :param daemon: 后台线程
    :param name: 新线程名字

    """

    # noinspection PyShadowingNames
    def wrapper(*args):
        try:
            func(*args)
        except Exception as e:
            logger.error(f"线程发生错误 {name}: {e}")

    t = Thread(target=wrapper, args=args, daemon=daemon, name=name)
    t.start()


def set_priority(pid=None, priority=psutil.REALTIME_PRIORITY_CLASS):
    if pid is None:
        pid = os.getpid()

    p = psutil.Process(pid)

    p.nice(priority)


# noinspection PyUnusedLocal,PyArgumentList,DuplicatedCode
class ToolTip:
    def __init__(self, widget, text, switch):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.switch = switch
        self.switch.trace_add('write', self.update_tooltip_status)

        # 根据初始状态绑定事件
        if not self.switch.get():
            self.bind_tooltip()

    def bind_tooltip(self):
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def unbind_tooltip(self):
        self.widget.unbind("<Enter>")
        self.widget.unbind("<Leave>")

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 35
        y += self.widget.winfo_rooty() + 35

        self.tooltip_window = ttk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip_window, bootstyle='inverse-light', text=self.text, relief="solid", borderwidth=1, padding=(5, 1))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def update_tooltip_status(self, *args):
        if self.switch.get():
            self.unbind_tooltip()
        else:
            self.bind_tooltip()


# noinspection PyArgumentList
class CollapsingFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.img_down = icon_to_image("angle-double-down", fill="#FFFFFF", scale_to_height=ICO_SIZE)
        self.img_up = icon_to_image("angle-double-up", fill="#FFFFFF", scale_to_height=ICO_SIZE)

    def add(self, child, title="", bootstyle=PRIMARY, image='', display=0, **kwargs):
        if child.winfo_class() != 'TFrame':
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

    def _toggle_open_close(self, child):
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.img_up)
        else:
            child.grid()
            child.btn.configure(image=self.img_down)

        self.update_size()

    def update_size(self):
        self.update_idletasks()
        plug_height = 30 if mini_skin_config else 62
        new_height = sum(c.winfo_height() for c in self.grid_slaves()) + plug_height
        # noinspection PyUnresolvedReferences
        self.master.geometry(f"{self.master.winfo_width()}x{new_height}")


# noinspection PyArgumentList,PyTypeChecker,DuplicatedCode
class BrutalityExtractor:
    """
    软件名：BrutalityExtractor\n
    版本：1.0.2\n
    更新时间：2023.06.14\n
    打包命令：pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --collect-all="tksvg" BrutalityExtractor.py\n
    TK 文档：https://docs.python.org/zh-cn/3.10/library/tk.html\n
    UI 文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/\n
    图标来源：https://fontawesome.com/v5/search?o=r&m=free&f=brands%2Cclassic\n
    """

    def __init__(self):
        # 主窗口配置
        self.root = ttk.Window()
        self.style = ttk.Style(theme=theme_config)
        self.root.title("BrutalityExtractor v1.0.2")
        self.root.attributes("-alpha", alpha_config)
        self.root.resizable(width=True, height=False)
        self.root.place_window_center()
        self.root.minsize(550, 1)
        self.root.iconbitmap(create_temp_icon_file(MAIN_ICO, logger))
        # self.root.grid_columnconfigure(0, weight=1)
        # self.root.grid_rowconfigure(10, weight=1)
        # self.root.geometry('550x600')
        # self.root.overrideredirect(True)
        # self.default_font = ttk.font.nametofont('TkDefaultFont')
        # self.default_font['size'] = 9
        # print(type(self.style.theme.colors.primary))

        # 定义回调
        self.digit_func = self.root.register(is_numeric)
        self.alpha_func = self.root.register(is_alpha)
        self.empty_func = self.root.register(is_not_empty)

        # 选择对话框
        def select_file(entry, var):
            file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("INI files", "*.ini"), ("CSV files", "*.csv"), ("All files", "*.*")))
            if file_path:
                var.set(file_path)
                entry.delete(0, END)
                entry.insert(0, file_path)
                entry.configure(foreground='black')

        def select_directory(entry, var):
            dir_path = filedialog.askdirectory()
            if dir_path:
                var.set(dir_path)
                entry.delete(0, END)
                entry.insert(0, dir_path)
                entry.configure(foreground='black')

        # 日志等级选择菜单样式更改
        # noinspection PyUnusedLocal
        def update_logl_style(*args):
            selected_option = self.var_logl.get()
            if selected_option == 'ERROR':
                self.menubutton_logl.config(bootstyle="danger-outline")
            elif selected_option == 'WARNING':
                self.menubutton_logl.config(bootstyle="warning-outline")
            elif selected_option == 'INFO':
                self.menubutton_logl.config(bootstyle="info-outline")
            else:
                self.menubutton_logl.config(bootstyle="dark-outline")

        # 写入配置
        # noinspection PyUnusedLocal
        def on_option_change(*args, config_key='', config_var=ttk.StringVar()):
            CP.set('main', config_key, str(config_var.get()))
            write_config(r'config/config.ini', CP, logger)

        # 修改主题
        def change_theme(theme):
            self.style.theme_use(theme)
            self.var_theme.set(theme)

        # 修改语言
        def change_language(lang):
            self.var_lang.set(lang)
            Messagebox.show_info(
                title=LANG['msg_info_title'],
                message=LANG['change_language_msg']
            )

        # 修改透明度
        def change_alpha(var):
            self.root.attributes("-alpha", var)

        # 文本框右键弹出窗口
        def create_right_click_menu(widget):
            def rightClick(event):
                rightClick_Menu = ttk.Menu(None, tearoff=1, takefocus=0)
                rightClick_Menu.add_command(label=LANG["RM_cut"], command=lambda: widget.event_generate('<<Cut>>'))
                rightClick_Menu.add_command(label=LANG["RM_copy"], command=lambda: widget.event_generate('<<Copy>>'))
                rightClick_Menu.add_command(label=LANG["RM_paste"], command=lambda: widget.event_generate('<<Paste>>'))
                rightClick_Menu.add_separator()
                rightClick_Menu.add_command(label=LANG["RM_select_all"], command=lambda: widget.event_generate('<<SelectAll>>'))
                rightClick_Menu.add_command(label=LANG["RM_delete"], command=lambda: widget.event_generate('<<Clear>>'))
                if isinstance(widget, ttk.Text):
                    rightClick_Menu.add_command(label=LANG["RM_undo"], command=lambda: widget.event_generate('<<Undo>>'))
                    rightClick_Menu.add_command(label=LANG["RM_redo"], command=lambda: widget.event_generate('<<Redo>>'))
                rightClick_Menu.tk_popup(event.x_root, event.y_root)

            widget.bind("<Button-3>", rightClick)

        # 建立变量函数
        def create_config_var(value, config_key):
            if isinstance(value, int):
                var = ttk.IntVar(value=value)
            elif isinstance(value, float):
                var = ttk.DoubleVar(value=value)
            else:
                var = ttk.StringVar(value=value)

            # noinspection PyTypeChecker
            var.trace_add("write", partial(on_option_change, config_key=config_key, config_var=var))

            return var

        cf = CollapsingFrame(self.root)
        cf.pack(fill=BOTH)

        # 先定义关闭通知变量
        self.var_ntlp = create_config_var(no_tooltip_config, 'no_tooltip')

        ## 基础配置区域
        self.basic_area = ttk.Frame(cf, padding=0)
        self.basic_area.columnconfigure(1, weight=1)
        self.img_basic_area = icon_to_image("cog", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.basic_area, title=LANG["basic_area_title"], display=1, image=self.img_basic_area, bootstyle="primary")

        # 解压目录相关元素
        self.var_path = create_config_var(path_zip_config, 'path_zip')

        self.label_path = ttk.Label(self.basic_area, text=LANG["label_path_text"])
        self.label_path.grid(row=1, column=0, sticky=E, padx=(15, 0), pady=(15, 0))

        self.entry_path = ttk.Entry(self.basic_area, bootstyle="dark", textvariable=self.var_path, validate="focus", validatecommand=(self.empty_func, '%P'))
        self.entry_path.grid(row=1, column=1, sticky=W + E, padx=(0, 0), pady=(15, 0))
        create_right_click_menu(self.entry_path)

        self.bottom_path = ttk.Button(self.basic_area, text=LANG["bottom_path_text"], bootstyle="secondary-outline", command=lambda: select_directory(self.entry_path, self.var_path))
        self.bottom_path.grid(row=1, column=2, sticky=E, padx=(10, 15), pady=(15, 0))

        ToolTip(self.label_path, LANG["tooltip_label_path"], self.var_ntlp)
        ToolTip(self.bottom_path, LANG["tooltip_bottom_path"], self.var_ntlp)

        # 目标目录相关元素
        self.var_dest = create_config_var(path_dest_config, 'path_dest')

        self.label_dest = ttk.Label(self.basic_area, text=LANG["label_dest_text"])
        self.label_dest.grid(row=2, column=0, sticky=E, padx=(15, 0), pady=(15, 0))

        self.entry_dest = ttk.Entry(self.basic_area, textvariable=self.var_dest, validate="focus")
        self.entry_dest.grid(row=2, column=1, sticky=W + E, padx=(0, 0), pady=(15, 0))
        create_right_click_menu(self.entry_dest)

        self.bottom_dest = ttk.Button(self.basic_area, text=LANG["bottom_path_text"], bootstyle="secondary-outline", command=lambda: select_directory(self.entry_dest, self.var_dest))
        self.bottom_dest.grid(row=2, column=2, sticky=E, padx=(10, 15), pady=(15, 0))

        ToolTip(self.label_dest, LANG["tooltip_label_dest"], self.var_ntlp)
        ToolTip(self.bottom_dest, LANG["tooltip_bottom_path"], self.var_ntlp)

        # 密码输入相关元素
        self.var_pass = create_config_var(password_config, 'password')

        self.label_pass = ttk.Label(self.basic_area, text=LANG["label_pass_text"])
        self.label_pass.grid(row=3, column=0, sticky=E, padx=(15, 0), pady=(15, 15))

        self.entry_pass = ttk.Entry(self.basic_area, textvariable=self.var_pass, validate="focus", validatecommand=('', '%P'))
        self.entry_pass.grid(row=3, column=1, sticky=W + E, padx=(0, 0), pady=(15, 15))
        create_right_click_menu(self.entry_pass)

        self.bottom_pass = ttk.Button(self.basic_area, text=LANG["bottom_pass_text"], bootstyle="secondary-outline", command=lambda: select_file(self.entry_pass, self.var_pass))
        self.bottom_pass.grid(row=3, column=2, sticky=E, padx=(10, 15), pady=(15, 15))

        ToolTip(self.label_pass, LANG["tooltip_label_pass"], self.var_ntlp)
        ToolTip(self.bottom_pass, LANG["tooltip_bottom_pass"], self.var_ntlp)

        ## 高级配置区块
        self.advance_area = ttk.Frame(cf, padding=0)
        # self.advance_area.columnconfigure(0, weight=1)
        self.img_advance_area = icon_to_image("cogs", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.advance_area, title=LANG["advance_area_title"], image=self.img_advance_area, bootstyle="warning")

        # 变换布局行1
        self.advance_area_fr1 = ttk.Frame(self.advance_area)
        self.advance_area_fr1.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 进程数量相关元素
        self.var_para = create_config_var(parallel_config, 'parallel')

        self.label_para = ttk.Label(self.advance_area_fr1, text=LANG["label_para_text"])
        self.label_para.pack(side=ttk.LEFT)

        self.spinbox_para = ttk.Spinbox(self.advance_area_fr1, textvariable=self.var_para, from_=1, to=round(cpu_count() / 2) if cpu_count() > 3 else 1, increment=1, width=3, state="readonly")
        self.spinbox_para.pack(side=ttk.LEFT)

        ToolTip(self.label_para, LANG["tooltip_label_para"], self.var_ntlp)

        # 变换布局行2
        self.advance_area_fr2 = ttk.Frame(self.advance_area)
        self.advance_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 忽略警告相关元素
        self.var_warn = create_config_var(no_warnning_config, 'no_warnning')

        self.label_warn = ttk.Label(self.advance_area_fr2, text=LANG["label_warn_text"])
        self.label_warn.pack(side=ttk.LEFT)

        self.checkbutton_warn = ttk.Checkbutton(self.advance_area_fr2, bootstyle="warning-square-toggle", variable=self.var_warn, onvalue=1, offvalue=0)
        self.checkbutton_warn.pack(side=ttk.LEFT)

        ToolTip(self.label_warn, LANG["tooltip_label_warn"], self.var_ntlp)

        # 释放空间相关元素
        self.var_sdlt = create_config_var(is_delete_config, 'is_delete')

        self.label_sdlt = ttk.Label(self.advance_area_fr2, text=LANG["label_sdlt_text"])
        self.label_sdlt.pack(side=ttk.LEFT, padx=(10, 0))

        self.checkbutton_sdlt = ttk.Checkbutton(self.advance_area_fr2, bootstyle="success-square-toggle", variable=self.var_sdlt, onvalue=1, offvalue=0)
        self.checkbutton_sdlt.pack(side=ttk.LEFT)

        ToolTip(self.label_sdlt, LANG["tooltip_label_sdlt"], self.var_ntlp)

        # 变换布局行3
        self.advance_area_fr3 = ttk.Frame(self.advance_area)
        self.advance_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))

        # 日志等级相关元素
        self.var_logl = create_config_var(log_level_config, 'log_level')
        self.var_logl.trace_add('write', update_logl_style)

        self.label_logl = ttk.Label(self.advance_area_fr3, text=LANG["label_logl_text"])
        self.label_logl.pack(side=ttk.LEFT)

        self.menubutton_logl = ttk.Menubutton(self.advance_area_fr3, bootstyle="default-outline", width=9, textvariable=self.var_logl)
        self.menubutton_logl.pack(side=ttk.LEFT)

        self.menu_logl = ttk.Menu(self.menubutton_logl, tearoff=True)
        self.menu_logl.add_radiobutton(label='ERROR', value='ERROR', variable=self.var_logl)
        self.menu_logl.add_radiobutton(label='WARNING', value='WARNING', variable=self.var_logl)
        self.menu_logl.add_radiobutton(label='INFO', value='INFO', variable=self.var_logl)
        self.menu_logl.add_radiobutton(label='DEBUG', value='DEBUG', variable=self.var_logl)

        self.menubutton_logl['menu'] = self.menu_logl
        update_logl_style()
        ToolTip(self.label_logl, LANG["tooltip_label_logl"], self.var_ntlp)

        # 日志大小相关元素
        self.var_logs = create_config_var(log_size_config, 'log_size')

        self.label_logs = ttk.Label(self.advance_area_fr3, text=LANG["label_logs_text"])
        self.label_logs.pack(side=ttk.LEFT, padx=(10, 0))

        self.spinbox_logs = ttk.Spinbox(self.advance_area_fr3, textvariable=self.var_logs, from_=1, to=10, increment=1, width=2, state="readonly")
        self.spinbox_logs.pack(side=ttk.LEFT)

        ToolTip(self.label_logs, LANG["tooltip_label_logs"], self.var_ntlp)

        # 日志数量相关元素
        self.var_logc = create_config_var(log_count_config, 'log_count')

        self.label_logc = ttk.Label(self.advance_area_fr3, text=LANG["label_logc_text"])
        self.label_logc.pack(side=ttk.LEFT, padx=(10, 0))

        self.spinbox_logc = ttk.Spinbox(self.advance_area_fr3, textvariable=self.var_logc, from_=1, to=99, increment=1, width=2, state="readonly")
        self.spinbox_logc.pack(side=ttk.LEFT)

        ToolTip(self.label_logc, LANG["tooltip_label_logc"], self.var_ntlp)

        ## 外观配置区块
        self.skin_area = ttk.Frame(cf, padding=0)
        # self.skin_area.columnconfigure(1, weight=1)
        # self.skin_area.rowconfigure(0, weight=1)
        self.img_skin_area = icon_to_image("palette", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.skin_area, title=LANG["skin_area_text"], image=self.img_skin_area, bootstyle="success")

        # 变换布局行1
        self.skin_area_fr1 = ttk.Frame(self.skin_area)
        self.skin_area_fr1.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 关闭提示相关元素
        self.label_ntlp = ttk.Label(self.skin_area_fr1, text=LANG["label_ntlp_text"])
        self.label_ntlp.pack(side=ttk.LEFT)

        self.checkbutton_ntlp = ttk.Checkbutton(self.skin_area_fr1, bootstyle="success-square-toggle", variable=self.var_ntlp, onvalue=1, offvalue=0)
        self.checkbutton_ntlp.pack(side=ttk.LEFT)

        ToolTip(self.label_ntlp, LANG["tooltip_label_ntlp"], self.var_ntlp)

        # 迷你模式相关元素
        self.var_mini = create_config_var(mini_skin_config, 'mini_skin')

        self.label_mini = ttk.Label(self.skin_area_fr1, text=LANG["label_mini_text"])
        self.label_mini.pack(side=ttk.LEFT, padx=(10, 0))

        self.checkbutton_mini = ttk.Checkbutton(self.skin_area_fr1, bootstyle="success-square-toggle", variable=self.var_mini, onvalue=1, offvalue=0)
        self.checkbutton_mini.pack(side=ttk.LEFT)

        ToolTip(self.label_mini, LANG["tooltip_label_mini"], self.var_ntlp)

        # 变换布局行2
        self.skin_area_fr2 = ttk.Frame(self.skin_area)
        self.skin_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 修改主题相关元素
        self.var_theme = create_config_var(theme_config, 'theme')

        self.label_theme = ttk.Label(self.skin_area_fr2, text=LANG["label_theme_text"])
        self.label_theme.pack(side=ttk.LEFT)

        self.menubutton_theme = ttk.Menubutton(self.skin_area_fr2, bootstyle="default-outline", width=9, textvariable=self.var_theme)
        self.menubutton_theme.pack(side=ttk.LEFT)

        self.menu_theme = ttk.Menu(self.menubutton_theme, tearoff=False)

        for item in THEME_LIST:
            self.menu_theme.add_command(label=item, command=lambda theme=item: change_theme(theme))
        self.menubutton_theme.configure(menu=self.menu_theme)
        ToolTip(self.label_theme, LANG["tooltip_label_theme"], self.var_ntlp)

        # 修改语言相关元素
        self.var_lang = create_config_var(lang_config, 'lang')

        self.label_lang = ttk.Label(self.skin_area_fr2, text=LANG["label_lang_text"])
        self.label_lang.pack(side=ttk.LEFT, padx=(10, 0))

        self.menubutton_lang = ttk.Menubutton(self.skin_area_fr2, bootstyle="default-outline", width=9, textvariable=self.var_lang)
        self.menubutton_lang.pack(side=ttk.LEFT)

        self.menu_lang = ttk.Menu(self.menubutton_lang, tearoff=False)
        self.menu_lang.add_command(label='English', command=lambda lang='ENG': change_language(lang))
        self.menu_lang.add_command(label='简体中文', command=lambda lang='CHS': change_language(lang))

        self.menubutton_lang.configure(menu=self.menu_lang)
        ToolTip(self.label_lang, LANG["tooltip_label_lang"], self.var_ntlp)

        # 变换布局行3
        self.skin_area_fr3 = ttk.Frame(self.skin_area)
        self.skin_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))

        # 窗口透明相关元素
        self.var_alpha = create_config_var(alpha_config, 'alpha')

        self.label_alpha = ttk.Label(self.skin_area_fr3, text=LANG["label_alpha_text"])
        self.label_alpha.pack(side=ttk.LEFT)

        self.scale_alpha = ttk.Scale(self.skin_area_fr3, bootstyle='success', variable=self.var_alpha, from_=0.20, to=1.00, command=lambda var=self.var_alpha.get(): change_alpha(var))
        self.scale_alpha.pack(side=ttk.LEFT)

        ToolTip(self.label_alpha, LANG["tooltip_label_alpha"], self.var_ntlp)

        ## 附加功能区块
        self.extra_area = ttk.Frame(cf, padding=0)
        self.extra_area.columnconfigure(1, weight=1)
        self.extra_area.rowconfigure(0, weight=1)
        self.img_extra_area = icon_to_image("brain", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.extra_area, title=LANG["extra_area_title"], image=self.img_extra_area, bootstyle="info")

        # 变换布局行1
        self.extra_area_fr1 = ttk.Frame(self.extra_area)
        self.extra_area_fr1.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 功能开关相关元素
        self.var_extr = create_config_var(is_extra_config, 'is_extra')

        self.label_extr = ttk.Label(self.extra_area_fr1, text=LANG["label_extr_text"])
        self.label_extr.pack(side=ttk.LEFT)

        self.checkbutton_extr = ttk.Checkbutton(self.extra_area_fr1, width=1, bootstyle="info-square-toggle", variable=self.var_extr, onvalue=1, offvalue=0)
        self.checkbutton_extr.pack(side=ttk.LEFT)

        ToolTip(self.label_extr, LANG["tooltip_label_extr"], self.var_ntlp)

        # 变换布局行2
        self.extra_area_fr2 = ttk.Frame(self.extra_area)
        self.extra_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 消除冗余相关元素
        self.var_rddd = create_config_var(is_redundant_config, 'is_redundant')

        self.label_rddd = ttk.Label(self.extra_area_fr2, text=LANG["label_rddd_text"])
        self.label_rddd.pack(side=ttk.LEFT)

        self.checkbutton_rddd = ttk.Checkbutton(self.extra_area_fr2, width=1, bootstyle="success-square-toggle", variable=self.var_rddd, onvalue=1, offvalue=0)
        self.checkbutton_rddd.pack(side=ttk.LEFT)

        ToolTip(self.label_rddd, LANG["tooltip_label_rddd"], self.var_ntlp)

        # 清理目录相关元素
        self.var_mpty = create_config_var(is_empty_config, 'is_empty')

        self.label_mpty = ttk.Label(self.extra_area_fr2, text=LANG["label_mpty_text"])
        self.label_mpty.pack(side=ttk.LEFT)

        self.checkbutton_mpty = ttk.Checkbutton(self.extra_area_fr2, bootstyle="success-square-toggle", variable=self.var_mpty, onvalue=1, offvalue=0)
        self.checkbutton_mpty.pack(side=ttk.LEFT)

        ToolTip(self.label_mpty, LANG["tooltip_label_mpty"], self.var_ntlp)

        # 变换布局行3
        self.extra_area_fr3 = ttk.Frame(self.extra_area)
        self.extra_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))
        self.extra_area_fr3.columnconfigure(1, weight=1)

        # 排除目录相关元素
        self.var_xcld = create_config_var(xcl_dir_config, 'xcl_dir')

        self.label_xcld = ttk.Label(self.extra_area_fr3, text=LANG["label_xcld_text"])
        self.label_xcld.grid(row=1, column=0, sticky=E, padx=(0, 0), pady=(0, 0))

        self.entry_xcld = ttk.Entry(self.extra_area_fr3, textvariable=self.var_xcld, validate="focus", validatecommand=('', '%P'))
        self.entry_xcld.grid(row=1, column=1, sticky=W + E, padx=(0, 0), pady=(0, 0))
        create_right_click_menu(self.entry_xcld)

        self.bottom_xcld = ttk.Button(self.extra_area_fr3, text=LANG["bottom_pass_text"], bootstyle="secondary-outline", command=lambda: select_file(self.entry_xcld, self.var_xcld))
        self.bottom_xcld.grid(row=1, column=2, sticky=E, padx=(10, 0), pady=(0, 0))

        ToolTip(self.label_xcld, LANG["tooltip_label_xcld"], self.var_ntlp)
        ToolTip(self.bottom_xcld, LANG["tooltip_bottom_xcld"], self.var_ntlp)

        # 排除文件相关元素
        self.var_xclf = create_config_var(xcl_file_config, 'xcl_file')

        self.label_xclf = ttk.Label(self.extra_area_fr3, text=LANG["label_xclf_text"])
        self.label_xclf.grid(row=2, column=0, sticky=E, padx=(0, 0), pady=(15, 0))

        self.entry_xclf = ttk.Entry(self.extra_area_fr3, textvariable=self.var_xclf, validate="focus", validatecommand=('', '%P'))
        self.entry_xclf.grid(row=2, column=1, sticky=W + E, padx=(0, 0), pady=(15, 0))
        create_right_click_menu(self.entry_xclf)

        self.bottom_xclf = ttk.Button(self.extra_area_fr3, text=LANG["bottom_pass_text"], bootstyle="secondary-outline", command=lambda: select_file(self.entry_xclf, self.var_xclf))
        self.bottom_xclf.grid(row=2, column=2, sticky=E, padx=(10, 0), pady=(15, 0))

        ToolTip(self.label_xclf, LANG["tooltip_label_xclf"], self.var_ntlp)
        ToolTip(self.bottom_xclf, LANG["tooltip_bottom_xclf"], self.var_ntlp)

        ## 显示日志区块
        self.log_area = ttk.Frame(cf, padding=0)
        # self.log_area.columnconfigure(0, weight=1)
        self.img_log_area = icon_to_image("outdent", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.log_area, title=LANG["log_area_title"], image=self.img_log_area, bootstyle="secondary")

        # 变换布局行1
        self.log_area_fr1 = ttk.Frame(self.log_area)
        self.log_area_fr1.pack(fill=tk.X)
        self.log_area_fr1.columnconfigure(0, weight=1)

        # 结果显示文本框相关元素
        self.text_logs = tk.Text(self.log_area_fr1, wrap=NONE, height=15, width=56, undo=True)
        self.text_logs.grid(row=0, column=0, sticky=W + E + N + S)
        self.text_logs.tag_config("red", foreground="#f04124")
        self.text_logs.tag_config("green", foreground="#43ac6a")

        self.text_logs_scrollbar = ttk.Scrollbar(self.log_area_fr1, bootstyle="light")
        self.text_logs_scrollbar.grid(row=0, column=0, sticky=E + N + S, rowspan=3, pady=(1, 1))
        self.text_logs_scrollbar.configure(command=self.text_logs.yview)
        self.text_logs.configure(yscrollcommand=self.text_logs_scrollbar.set)

        create_right_click_menu(self.text_logs)

        ## 各种按钮区块
        self.frame_bottom = ttk.Frame(self.root, bootstyle="light")
        self.frame_bottom.pack(fill='x')
        self.frame_bottom.columnconfigure(6, weight=200)

        # 项目主页相关元素
        self.img_github = icon_to_image("github", fill="#008cba", scale_to_height=ICO_SIZE)
        self.bottom_github = ttk.Button(self.frame_bottom, text=LANG["bottom_github_text"], image=self.img_github, bootstyle="light-outline", cursor='heart',
                                        command=lambda: webbrowser.open("https://github.com/hxz393/BrutalityExtractor", new=0))
        self.bottom_github.grid(row=0, column=0, sticky='E')
        ToolTip(self.bottom_github, LANG["bottom_github_text"], self.var_ntlp)

        # 检查更新相关元素
        self.img_update = icon_to_image("sync-alt", fill="#008cba", scale_to_height=ICO_SIZE)
        self.bottom_update = ttk.Button(self.frame_bottom, text=LANG["bottom_update_text"], image=self.img_update, bootstyle="light-outline", command=lambda: thread_it(self.check_update, ))
        self.bottom_update.grid(row=0, column=1, sticky='E')
        ToolTip(self.bottom_update, LANG["bottom_update_text"], self.var_ntlp)

        # 打开日志相关元素
        self.img_logpath = icon_to_image("envelope-open-text", fill="#008cba", scale_to_height=ICO_SIZE)
        self.bottom_logpath = ttk.Button(self.frame_bottom, text=LANG["bottom_logpath_text"], image=self.img_logpath, bootstyle="light-outline", command=lambda: os.startfile('logs'))
        self.bottom_logpath.grid(row=0, column=2, sticky='E')
        ToolTip(self.bottom_logpath, LANG["bottom_logpath_text"], self.var_ntlp)

        # 开始运行按钮
        self.img_run = icon_to_image("play", fill="#FFFFFF", scale_to_height=ICO_SIZE)
        self.img_wait = icon_to_image("clock", fill=self.style.theme.colors.primary, scale_to_height=ICO_SIZE)
        self.bottom_run = ttk.Button(self.frame_bottom, text=LANG["bottom_run_text"], image=self.img_run, bootstyle="danger", command=lambda: thread_it(self.main, ))
        self.bottom_run.config(compound=LEFT) if self.var_mini.get() else NONE
        self.bottom_run.grid(row=0, column=6, sticky='WE')
        ToolTip(self.bottom_run, LANG["bottom_run_text"], self.var_ntlp)

        # self.bottom_run.config(style='Large.TButton',)
        # self.style.configure('Large.TButton', font=(None, 16))

        # 定义变量
        self.var_logl.set('INFO') if self.var_logl.get() not in LOG_LEVEL_LIST else None
        self.var_lang.set('ENG') if self.var_lang.get() not in LANG_LIST else None

    # 检查更新函数
    def check_update(self):
        current_version = self.root.title()
        self.bottom_update['stat'] = 'disabled'
        url = "https://blog.x2b.net/ver/brutalityextractorversion.txt"
        session = requests.Session()
        session.trust_env = False
        urllib3.disable_warnings()

        try:
            response = session.get(url, verify=False)
            if response.status_code == 200:
                latest_version = response.text.strip()
                if latest_version != current_version:
                    self.root.after(10, lambda: Messagebox.show_info(
                        title=LANG["msg_info_title"],
                        message=LANG["check_update_info_1"].format(current_version, latest_version)
                    ))
                elif latest_version == current_version:
                    self.root.after(10, lambda: Messagebox.show_info(
                        title=LANG["msg_info_title"],
                        message=LANG["check_update_info_2"].format(current_version, latest_version)
                    ))
            else:
                self.root.after(10, lambda: Messagebox.show_info(
                    title=LANG['msg_info_title'],
                    message=LANG["check_update_info_3"]
                ))
        except Exception as e:
            logger.error(LANG["check_update_error_log"].format(url, e))
            self.root.after(10, lambda: Messagebox.show_error(
                title=LANG["msg_error_title"],
                message=LANG["check_update_error_msg"]
            ))

        finally:
            self.bottom_update['stat'] = 'normal'

    # 附加功能函数
    def extra(self):
        path_dest = self.entry_dest.get()
        xcld = set(read_txt_to_list(self.entry_xcld.get(), logger) if os.path.isfile(self.entry_xcld.get()) else [self.entry_xcld.get()])
        xclf = set(read_txt_to_list(self.entry_xclf.get(), logger) if os.path.isfile(self.entry_xclf.get()) else [self.entry_xclf.get()])
        is_redundant = self.var_rddd.get()
        is_empty = self.var_mpty.get()

        logger.info(LANG["extra_info_start"].format("#" * 6, "#" * 6))

        if not path_dest:
            logger.warning(LANG["extra_path_dest_warning"].format("#" * 6, "#" * 6))
            self.root.after(10, lambda: Messagebox.show_warning(
                title=LANG['msg_info_title'],
                message=LANG["extra_path_dest_warning_msg"]))
            return

        if not get_folder_paths(path_dest, logger) and not get_file_paths(path_dest, logger):
            self.text_logs.insert(END, LANG["extra_no_action"].format(path_dest), "green")
            return

        if xcld != {''}:
            paths = get_folder_paths(path_dest, logger)
            remove_matched(paths, logger, xcld)
            del_count = len(paths) - len(get_folder_paths(path_dest, logger))
            self.text_logs.insert(END, LANG["extra_xcld_info"].format(path_dest, del_count), "green")

        if xclf != {''}:
            files = get_file_paths(path_dest, logger)
            remove_matched(files, logger, xclf)
            del_count = len(files) - len(get_file_paths(path_dest, logger))
            self.text_logs.insert(END, LANG["extra_xclf_info"].format(path_dest, del_count), "green")

        if is_redundant:
            paths = get_folder_paths(path_dest, logger)
            [remove_redundant(i, logger) for i in get_subdirectories(path_dest, logger)]
            del_count = len(paths) - len(get_folder_paths(path_dest, logger))
            self.text_logs.insert(END, LANG["extra_is_redundant_info"].format(path_dest, del_count), "green")

        if is_empty:
            paths = get_folder_paths(path_dest, logger)
            remove_empty_dirs(path_dest, logger)
            del_count = len(paths) - len(get_folder_paths(path_dest, logger))
            self.text_logs.insert(END, LANG["extra_is_empty_info"].format(path_dest, del_count), "green")

        logger.info(LANG["extra_info_done"].format("#" * 6, "#" * 6))

    # 主函数
    def main(self):
        # 初始化变量
        password = set(read_txt_to_list(self.entry_pass.get(), logger) if os.path.isfile(self.entry_pass.get()) else [self.entry_pass.get()])
        path_zip = self.entry_path.get()
        path_dest = self.entry_dest.get()
        no_warnning = self.var_warn.get()
        is_delete = self.var_sdlt.get()
        is_extra = self.var_extr.get()

        start_time = time.time()
        failed_counts = 0
        finished_counts = 0

        self.text_logs.delete(1.0, END)

        try:
            # 执行附加功能
            if is_extra:
                self.bottom_run.config(state='disabled')
                self.bottom_run.config(text=LANG["extra_bottom_run_text"])
                self.bottom_run.config(image=self.img_wait)

                self.extra()
                return

            # 切换按钮类型
            var_prog = ttk.IntVar()
            self.bottom_run = ttk.Progressbar(self.frame_bottom, orient="horizontal", mode="determinate", variable=var_prog, bootstyle="success")
            self.bottom_run.grid(row=0, column=6, sticky='WENS')

            logger.info(LANG["main_info_start"].format("#" * 6, "#" * 6))

            # 检查目录
            if not path_zip:
                logger.warning(LANG["main_no_path_zip_warning"].format("#" * 6, "#" * 6))
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_info_title'],
                    message=LANG["main_no_path_zip_warning_msg"]))
                return

            # 获取目标目录下的所有文件路径列表，检查是否有文件
            file_paths = get_file_paths(path_zip, logger)
            if not file_paths:
                logger.warning(LANG["main_no_file_warning"].format("#" * 6, path_zip, "#" * 6))
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_info_title'],
                    message=LANG["main_no_file_warning_msg"].format(path_zip)))
                return

            # 对文件路径列表按解压目标进行初步分组
            path_groups = group_file_paths(file_paths, logger)

            # 生成全文件分组列表，替换掉目标目录
            disk_free = psutil.disk_usage(Path(path_zip).anchor).free
            full_infos = group_list_by_lens(path_groups, logger)
            if path_dest:
                path_dest = Path(path_dest)
                try:
                    path_dest.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(LANG["main_path_dest_error"].format("#" * 6, path_dest, e))
                    self.root.after(10, lambda: Messagebox.show_error(
                        title=LANG['msg_error_title'],
                        message=LANG["main_path_dest_error_msg"].format(path_dest)))
                    return
                full_infos = [{**file_info, 'target_path': str(path_dest / Path(*Path(file_info['target_path']).parts[len(Path(path_zip).parts):]))} for file_info in full_infos]
                disk_free = psutil.disk_usage(Path(path_dest).anchor).free

            # 筛选出压缩文件分组列表，检查是否有压缩文件
            file_infos = group_files_main(full_infos, logger)
            if not file_infos:
                logger.warning(LANG["main_no_file_infos_warning"].format("#" * 6, path_zip, "#" * 6))
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_info_title'],
                    message=LANG["main_no_file_infos_warning_msg"].format(path_zip)))
                return

            # 计算变量
            file_size = sum(get_target_size(p, logger) for i in file_infos for p in i['file_list'])
            file_size_format = format_size(file_size)
            file_in_total_number = len(file_infos)
            self.bottom_run.configure(maximum=file_in_total_number)
            parallel = min(file_in_total_number, int(self.var_para.get()), round(cpu_count() / 2) if cpu_count() > 3 else 1)

            # 磁盘空间低警告
            if disk_free < file_size and not no_warnning:
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_warning_title'],
                    message=LANG["disk_free_warning"]))
                return

            # CPU 负载高警告
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > 50 and not no_warnning:
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_warning_title'],
                    message=LANG["cpu_usage_warning"]))
                return

            # 内存使用率高警告
            memory_usage = psutil.virtual_memory().percent
            if memory_usage > 70 and not no_warnning:
                self.root.after(10, lambda: Messagebox.show_warning(
                    title=LANG['msg_warning_title'],
                    message=LANG["memory_usage_warning"]))
                return

            def update_progress(total):
                value = var_prog.get()
                if value < total:
                    value += 1
                    var_prog.set(value)
                    self.bottom_run["value"] = value

            # 解压后操作
            def post_action(result):
                return_code = result['code']
                nonlocal failed_counts
                nonlocal finished_counts

                if return_code == 2:
                    remove_target(result['file_info']['target_path'], logger)
                    failed_counts += 1
                    self.text_logs.insert(END, result['std'] + '\n', "red")
                elif return_code == 0:
                    [remove_target(file_del, logger) for file_del in result['file_info']['file_list']] if is_delete == 1 else None
                    finished_counts += 1
                    self.text_logs.insert(END, result['std'] + '\n', "green")

                update_progress(file_in_total_number)

            # 多进程解压
            thread_pool = Pool(processes=parallel)
            for file_info in file_infos:
                thread_pool.apply_async(unzip, args=(file_info, password, logger), callback=post_action)
            thread_pool.close()
            thread_pool.join()

            # unzip(file_infos[0], password, logger)

            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_time_format = format_time(end_time - start_time)
            your_speed = calculate_speed(file_size, elapsed_time)

            logger.info(LANG["main_info_done"].format('#' * 6, '#' * 6, file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time_format, your_speed))
            self.root.after(10, lambda: Messagebox.ok(title=LANG["msg_info_title"], message=LANG["main_info_done_msg"].format(file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time_format, your_speed)))

        # 故障处理
        except Exception as e:
            logger.error(LANG["main_error"].format('#' * 6, '#' * 6, e))
            self.root.after(10, lambda: Messagebox.ok(title=LANG["msg_error_title"], message=LANG["main_error_msg"]))

        # 恢复按钮状态
        finally:
            self.bottom_run = ttk.Button(self.frame_bottom, text=LANG["bottom_run_text"], image=self.img_run, bootstyle="danger", command=lambda: thread_it(self.main, ))
            self.bottom_run.config(compound=LEFT) if self.var_mini.get() else NONE
            self.bottom_run.grid(row=0, column=6, sticky='WE')

    # 启动Tkinter
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    freeze_support()
    set_priority()
    if not CP:
        write_config(r'config/config.ini', {'main': {}}, logger)
        CP = read_config(r'config/config.ini', logger)
    app = BrutalityExtractor()
    app.run()
