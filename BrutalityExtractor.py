import os.path
import time
import tkinter as tk
import webbrowser
from multiprocessing import Pool, freeze_support, cpu_count

import psutil
import ttkbootstrap as ttk
from tkfontawesome import icon_to_image
from ttkbootstrap.constants import *

from modules import *

logger = logging.getLogger(__name__)
logging_config(**LOG_CONFIG_DICT)


# noinspection PyUnusedLocal,PyArgumentList
class BrutalityExtractor:
    """
    软件名：BrutalityExtractor\n
    版本：1.2.0\n
    更新时间：2023.06.28\n
    打包命令：pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --collect-all="tksvg" BrutalityExtractor.py\n
    TK 文档：https://docs.python.org/zh-cn/3.10/library/tk.html\n
    UI 文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/\n
    图标来源：https://fontawesome.com/v5/search?o=r&m=free&f=brands%2Cclassic\n
    """

    def __init__(self):
        # 主窗口配置
        self.root = ttk.Window()
        self.style = ttk.Style(theme=theme_config)
        self.root.title("BrutalityExtractor v1.2.0")
        self.root.attributes("-alpha", alpha_config)
        self.root.resizable(width=True, height=False)
        self.root.place_window_center()
        self.root.minsize(550, 1)
        self.root.iconbitmap(convert_base64_to_ico(MAIN_ICO))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.process_pool = None

        cf = CollapsingFrame(self.root)
        cf.pack(fill=BOTH)

        # 先定义关闭通知变量
        self.var_ntlp = ui_create_config_var(no_tooltip_config, 'no_tooltip')

        ## 基础配置区域
        self.basic_area = ttk.Frame(cf, padding=0)
        self.basic_area.columnconfigure(1, weight=1)
        self.img_basic_area = icon_to_image("cog", fill="#FFFFFF", scale_to_width=ICO_SIZE)
        cf.add(child=self.basic_area, title=LANG["basic_area_title"], display=1, image=self.img_basic_area, bootstyle="primary")

        # 解压目录相关元素
        self.var_path = ui_create_config_var(path_zip_config, 'path_zip')

        self.label_path = ttk.Label(self.basic_area, text=LANG["label_path_text"])
        self.label_path.grid(row=1, column=0, sticky=E, padx=(15, 0), pady=(15, 0))

        self.entry_path = ttk.Entry(self.basic_area, bootstyle="dark", textvariable=self.var_path, validate="focus")
        self.entry_path.grid(row=1, column=1, sticky=W + E, padx=(0, 0), pady=(15, 0))
        ui_create_right_click_menu(self.entry_path)

        self.bottom_path = ttk.Button(self.basic_area, text=LANG["bottom_path_text"], bootstyle="secondary-outline",
                                      command=lambda: ui_select_file_or_directory(self.entry_path, self.var_path, 'folder'))
        self.bottom_path.grid(row=1, column=2, sticky=E, padx=(10, 15), pady=(15, 0))

        ToolTip(self.label_path, LANG["tooltip_label_path"], self.var_ntlp)
        ToolTip(self.bottom_path, LANG["tooltip_bottom_path"], self.var_ntlp)

        # 目标目录相关元素
        self.var_dest = ui_create_config_var(path_dest_config, 'path_dest')

        self.label_dest = ttk.Label(self.basic_area, text=LANG["label_dest_text"])
        self.label_dest.grid(row=2, column=0, sticky=E, padx=(15, 0), pady=(15, 0))

        self.entry_dest = ttk.Entry(self.basic_area, textvariable=self.var_dest, validate="focus")
        self.entry_dest.grid(row=2, column=1, sticky=W + E, padx=(0, 0), pady=(15, 0))
        ui_create_right_click_menu(self.entry_dest)

        self.bottom_dest = ttk.Button(self.basic_area, text=LANG["bottom_path_text"], bootstyle="secondary-outline",
                                      command=lambda: ui_select_file_or_directory(self.entry_dest, self.var_dest, 'folder'))
        self.bottom_dest.grid(row=2, column=2, sticky=E, padx=(10, 15), pady=(15, 0))

        ToolTip(self.label_dest, LANG["tooltip_label_dest"], self.var_ntlp)
        ToolTip(self.bottom_dest, LANG["tooltip_bottom_path"], self.var_ntlp)

        # 密码输入相关元素
        self.var_pass = ui_create_config_var(password_config, 'password')

        self.label_pass = ttk.Label(self.basic_area, text=LANG["label_pass_text"])
        self.label_pass.grid(row=3, column=0, sticky=E, padx=(15, 0), pady=(15, 15))

        self.entry_pass = ttk.Entry(self.basic_area, textvariable=self.var_pass, validate="focus")
        self.entry_pass.grid(row=3, column=1, sticky=W + E, padx=(0, 0), pady=(15, 15))
        ui_create_right_click_menu(self.entry_pass)

        self.bottom_pass = ttk.Button(self.basic_area, text=LANG["bottom_pass_text"], bootstyle="secondary-outline",
                                      command=lambda: ui_select_file_or_directory(self.entry_pass, self.var_pass, 'file'))
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
        self.var_para = ui_create_config_var(parallel_config, 'parallel')

        self.label_para = ttk.Label(self.advance_area_fr1, text=LANG["label_para_text"])
        self.label_para.pack(side=ttk.LEFT)

        self.spinbox_para = ttk.Spinbox(self.advance_area_fr1, textvariable=self.var_para, from_=1, to=round(cpu_count() / 2) if cpu_count() > 3 else 1, increment=1, width=3, state="readonly")
        self.spinbox_para.pack(side=ttk.LEFT)

        ToolTip(self.label_para, LANG["tooltip_label_para"], self.var_ntlp)

        # 变换布局行2
        self.advance_area_fr2 = ttk.Frame(self.advance_area)
        self.advance_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 忽略警告相关元素
        self.var_warn = ui_create_config_var(no_warnning_config, 'no_warnning')

        self.label_warn = ttk.Label(self.advance_area_fr2, text=LANG["label_warn_text"])
        self.label_warn.pack(side=ttk.LEFT)

        self.checkbutton_warn = ttk.Checkbutton(self.advance_area_fr2, bootstyle="success-square-toggle", variable=self.var_warn, onvalue=1, offvalue=0)
        self.checkbutton_warn.pack(side=ttk.LEFT)

        ToolTip(self.label_warn, LANG["tooltip_label_warn"], self.var_ntlp)

        # 释放空间相关元素
        self.var_sdlt = ui_create_config_var(is_delete_config, 'is_delete')

        self.label_sdlt = ttk.Label(self.advance_area_fr2, text=LANG["label_sdlt_text"])
        self.label_sdlt.pack(side=ttk.LEFT, padx=(10, 0))

        self.checkbutton_sdlt = ttk.Checkbutton(self.advance_area_fr2, bootstyle="success-square-toggle", variable=self.var_sdlt, onvalue=1, offvalue=0)
        self.checkbutton_sdlt.pack(side=ttk.LEFT)

        ToolTip(self.label_sdlt, LANG["tooltip_label_sdlt"], self.var_ntlp)

        # 强制模式相关元素
        self.var_sfrc = ui_create_config_var(is_force_config, 'is_force')

        self.label_sfrc = ttk.Label(self.advance_area_fr2, text=LANG["label_sfrc_text"])
        self.label_sfrc.pack(side=ttk.LEFT, padx=(10, 0))

        self.checkbutton_sfrc = ttk.Checkbutton(self.advance_area_fr2, bootstyle="warning-square-toggle", variable=self.var_sfrc, onvalue=1, offvalue=0)
        self.checkbutton_sfrc.pack(side=ttk.LEFT)

        ToolTip(self.label_sfrc, LANG["tooltip_label_sfrc"], self.var_ntlp)

        # 变换布局行3
        self.advance_area_fr3 = ttk.Frame(self.advance_area)
        self.advance_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))

        # 日志等级相关元素
        self.var_logl = ui_create_config_var(log_level_config, 'log_level')
        self.var_logl.trace_add('write', self.update_logl_style)

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
        self.update_logl_style()
        ToolTip(self.label_logl, LANG["tooltip_label_logl"], self.var_ntlp)

        # 日志大小相关元素
        self.var_logs = ui_create_config_var(log_size_config, 'log_size')

        self.label_logs = ttk.Label(self.advance_area_fr3, text=LANG["label_logs_text"])
        self.label_logs.pack(side=ttk.LEFT, padx=(10, 0))

        self.spinbox_logs = ttk.Spinbox(self.advance_area_fr3, textvariable=self.var_logs, from_=1, to=10, increment=1, width=2, state="readonly")
        self.spinbox_logs.pack(side=ttk.LEFT)

        ToolTip(self.label_logs, LANG["tooltip_label_logs"], self.var_ntlp)

        # 日志数量相关元素
        self.var_logc = ui_create_config_var(log_count_config, 'log_count')

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
        self.var_mini = ui_create_config_var(mini_skin_config, 'mini_skin')

        self.label_mini = ttk.Label(self.skin_area_fr1, text=LANG["label_mini_text"])
        self.label_mini.pack(side=ttk.LEFT, padx=(10, 0))

        self.checkbutton_mini = ttk.Checkbutton(self.skin_area_fr1, bootstyle="success-square-toggle", variable=self.var_mini, onvalue=1, offvalue=0)
        self.checkbutton_mini.pack(side=ttk.LEFT)

        ToolTip(self.label_mini, LANG["tooltip_label_mini"], self.var_ntlp)

        # 变换布局行2
        self.skin_area_fr2 = ttk.Frame(self.skin_area)
        self.skin_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 修改主题相关元素
        self.var_theme = ui_create_config_var(theme_config, 'theme')

        self.label_theme = ttk.Label(self.skin_area_fr2, text=LANG["label_theme_text"])
        self.label_theme.pack(side=ttk.LEFT)

        self.menubutton_theme = ttk.Menubutton(self.skin_area_fr2, bootstyle="default-outline", width=9, textvariable=self.var_theme)
        self.menubutton_theme.pack(side=ttk.LEFT)

        self.menu_theme = ttk.Menu(self.menubutton_theme, tearoff=False)

        for item in THEME_LIST:
            self.menu_theme.add_command(label=item, command=lambda theme=item: self.change_theme(theme))
        self.menubutton_theme.configure(menu=self.menu_theme)
        ToolTip(self.label_theme, LANG["tooltip_label_theme"], self.var_ntlp)

        # 修改语言相关元素
        self.var_lang = ui_create_config_var(lang_config, 'lang')

        self.label_lang = ttk.Label(self.skin_area_fr2, text=LANG["label_lang_text"])
        self.label_lang.pack(side=ttk.LEFT, padx=(10, 0))

        self.menubutton_lang = ttk.Menubutton(self.skin_area_fr2, bootstyle="default-outline", width=9, textvariable=self.var_lang)
        self.menubutton_lang.pack(side=ttk.LEFT)

        self.menu_lang = ttk.Menu(self.menubutton_lang, tearoff=False)
        self.menu_lang.add_command(label='English', command=lambda lang='ENG': self.change_language(lang))
        self.menu_lang.add_command(label='简体中文', command=lambda lang='CHS': self.change_language(lang))

        self.menubutton_lang.configure(menu=self.menu_lang)
        ToolTip(self.label_lang, LANG["tooltip_label_lang"], self.var_ntlp)

        # 变换布局行3
        self.skin_area_fr3 = ttk.Frame(self.skin_area)
        self.skin_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))

        # 窗口透明相关元素
        self.var_alpha = ui_create_config_var(alpha_config, 'alpha')

        self.label_alpha = ttk.Label(self.skin_area_fr3, text=LANG["label_alpha_text"])
        self.label_alpha.pack(side=ttk.LEFT)

        self.scale_alpha = ttk.Scale(self.skin_area_fr3, bootstyle='success', variable=self.var_alpha, from_=0.20, to=1.00, command=lambda var=self.var_alpha.get(): self.change_alpha(var))
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
        self.var_extr = ui_create_config_var(is_extra_config, 'is_extra')

        self.label_extr = ttk.Label(self.extra_area_fr1, text=LANG["label_extr_text"])
        self.label_extr.pack(side=ttk.LEFT)

        self.checkbutton_extr = ttk.Checkbutton(self.extra_area_fr1, width=1, bootstyle="info-square-toggle", variable=self.var_extr, onvalue=1, offvalue=0)
        self.checkbutton_extr.pack(side=ttk.LEFT)

        ToolTip(self.label_extr, LANG["tooltip_label_extr"], self.var_ntlp)

        # 变换布局行2
        self.extra_area_fr2 = ttk.Frame(self.extra_area)
        self.extra_area_fr2.pack(fill=tk.X, padx=(15, 15), pady=(15, 0))

        # 消除冗余相关元素
        self.var_rddd = ui_create_config_var(is_redundant_config, 'is_redundant')

        self.label_rddd = ttk.Label(self.extra_area_fr2, text=LANG["label_rddd_text"])
        self.label_rddd.pack(side=ttk.LEFT)

        self.checkbutton_rddd = ttk.Checkbutton(self.extra_area_fr2, width=1, bootstyle="success-square-toggle", variable=self.var_rddd, onvalue=1, offvalue=0)
        self.checkbutton_rddd.pack(side=ttk.LEFT)

        ToolTip(self.label_rddd, LANG["tooltip_label_rddd"], self.var_ntlp)

        # 清理目录相关元素
        self.var_mpty = ui_create_config_var(is_empty_config, 'is_empty')

        self.label_mpty = ttk.Label(self.extra_area_fr2, text=LANG["label_mpty_text"])
        self.label_mpty.pack(side=ttk.LEFT)

        self.checkbutton_mpty = ttk.Checkbutton(self.extra_area_fr2, bootstyle="success-square-toggle", variable=self.var_mpty, onvalue=1, offvalue=0)
        self.checkbutton_mpty.pack(side=ttk.LEFT)

        ToolTip(self.label_mpty, LANG["tooltip_label_mpty"], self.var_ntlp)

        # 变换布局行3
        self.extra_area_fr3 = ttk.Frame(self.extra_area)
        self.extra_area_fr3.pack(fill=tk.X, padx=(15, 15), pady=(15, 15))
        self.extra_area_fr3.columnconfigure(1, weight=1)

        # 删除垃圾相关元素
        self.var_xclf = ui_create_config_var(xcl_file_config, 'xcl_file')

        self.label_xclf = ttk.Label(self.extra_area_fr3, text=LANG["label_xclf_text"])
        self.label_xclf.grid(row=2, column=0, sticky=E)

        self.entry_xclf = ttk.Entry(self.extra_area_fr3, textvariable=self.var_xclf, validate="focus")
        self.entry_xclf.grid(row=2, column=1, sticky=W + E)
        ui_create_right_click_menu(self.entry_xclf)

        self.bottom_xclf = ttk.Button(self.extra_area_fr3, text=LANG["bottom_pass_text"], bootstyle="secondary-outline",
                                      command=lambda: ui_select_file_or_directory(self.entry_xclf, self.var_xclf, 'file'))
        self.bottom_xclf.grid(row=2, column=2, sticky=E, padx=(10, 0))

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
        self.text_logs = tk.Text(self.log_area_fr1, wrap=NONE, height=8, width=56, undo=True)
        self.text_logs.grid(row=0, column=0, sticky=W + E + N + S)
        self.text_logs.tag_config("red", foreground="#f04124")
        self.text_logs.tag_config("green", foreground="#43ac6a")

        self.text_logs_scrollbar = ttk.Scrollbar(self.log_area_fr1, bootstyle="light")
        self.text_logs_scrollbar.grid(row=0, column=0, sticky=E + N + S, rowspan=3, pady=(1, 1))
        self.text_logs_scrollbar.configure(command=self.text_logs.yview)
        self.text_logs.configure(yscrollcommand=self.text_logs_scrollbar.set)

        ui_create_right_click_menu(self.text_logs)

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

    def update_logl_style(self, *args):
        """日志等级选择菜单样式更改"""
        log_level_styles = {
            'ERROR': 'danger-outline',
            'WARNING': 'warning-outline',
            'INFO': 'info-outline'
        }
        selected_option = self.var_logl.get()
        self.menubutton_logl.config(bootstyle=log_level_styles.get(selected_option, 'dark-outline'))

    def update_progress(self, total, var):
        """更新进度条"""
        value = var.get()
        if value < total:
            value += 1
            var.set(value)
            self.bottom_run["value"] = value

    def change_theme(self, theme):
        """修改主题"""
        self.style.theme_use(theme)
        self.var_theme.set(theme)

    def change_alpha(self, var):
        """修改透明度"""
        self.root.attributes("-alpha", var)

    # noinspection PyShadowingNames
    def change_language(self, lang):
        """修改语言"""
        self.var_lang.set(lang)
        LANG = LANG_DICT[lang]
        ui_display_msg(self.root, LANG["change_language_msg"], 'info')

    def check_update(self):
        """检查更新函数"""
        current_version = self.root.title()
        self.bottom_update['stat'] = 'disabled'
        latest_version = request_url(CHECK_UPDATE_URL)

        if latest_version is None:
            ui_display_msg(self.root, LANG["check_update_error_msg"], 'error')
        elif latest_version != current_version:
            ui_display_msg(self.root, LANG["check_update_info_1"].format(current_version, latest_version), 'info')
        elif latest_version == current_version:
            ui_display_msg(self.root, LANG["check_update_info_2"].format(current_version, latest_version), 'info')
        self.bottom_update['stat'] = 'normal'

    # noinspection PyShadowingNames
    def extra(self):
        """附加功能函数"""
        self.bottom_run.config(state='disabled')
        self.bottom_run.config(text=LANG["extra_bottom_run_text"])
        self.bottom_run.config(image=self.img_wait)
        logger.info(LANG["extra_info_start"].format("#" * 6, "#" * 6))

        try:
            path_dest = self.entry_dest.get().strip()
            xclf = self.entry_xclf.get().strip()
            xclf_list = read_file_to_list(xclf) if Path(xclf).is_file() else [xclf] if xclf else None
            is_redundant = self.var_rddd.get()
            is_empty = self.var_mpty.get()

            if not path_dest or not Path(path_dest).exists():
                ui_display_msg(self.root, LANG["extra_path_dest_warning_msg"], 'warning')
                logger.warning(LANG["extra_path_dest_warning_msg"])
                return None

            if not os.listdir(path_dest):
                self.text_logs.insert(END, LANG["extra_no_action"].format(path_dest), "green")
                logger.info(LANG["extra_no_action"].format(path_dest))
                return None

            if xclf_list:
                del_list = remove_target_matched(path_dest, xclf_list)
                del_count = len(del_list)
                self.text_logs.insert(END, LANG["extra_xclf_info"].format(path_dest, del_count), "green" if not del_count else "red")
                logger.info(LANG["extra_xclf_info"].format(path_dest, del_count))
                logger.debug(LANG["extra_debug_del_list"].format(list_to_str(del_list)))

            if is_redundant:
                del_list = remove_redundant_dirs(path_dest)
                del_count = len(del_list)
                self.text_logs.insert(END, LANG["extra_is_redundant_info"].format(path_dest, del_count), "green" if not del_count else "red")
                logger.info(LANG["extra_is_redundant_info"].format(path_dest, del_count))
                logger.debug(LANG["extra_debug_del_list"].format(list_to_str(del_list)))

            if is_empty:
                del_list = remove_empty_dirs(path_dest)
                del_count = len(del_list)
                self.text_logs.insert(END, LANG["extra_is_empty_info"].format(path_dest, del_count), "green" if not del_count else "red")
                logger.info(LANG["extra_is_empty_info"].format(path_dest, del_count))
                logger.debug(LANG["extra_debug_del_list"].format(list_to_str(del_list)))

            return True
        except Exception as e:
            logger.error("Error during deletion process: {}".format("#" * 6, e, "#" * 6))
            return None
        finally:
            logger.info(LANG["extra_info_done"].format("#" * 6, "#" * 6))

    # 主函数
    # noinspection PyShadowingNames
    def main(self):
        self.text_logs.delete(1.0, END)
        try:
            if self.var_extr.get():
                self.extra()
                return

            logger.info(LANG["main_info_start"].format("#" * 6, "#" * 6))

            # 变换按钮类型
            var_prog = ttk.IntVar()
            self.bottom_run = ttk.Progressbar(self.frame_bottom, orient="horizontal", mode="determinate", variable=var_prog, bootstyle="success")
            self.bottom_run.grid(row=0, column=6, sticky='WENS')

            # 检查解压目录是否正确
            path_zip = self.entry_path.get().strip()
            if not path_zip and not Path(path_zip).exists():
                logger.warning(LANG["main_no_path_zip_warning"].format("#" * 6, "#" * 6))
                ui_display_msg(self.root, LANG["main_no_path_zip_warning_msg"], 'warning')
                return

            # 获取到目标目录下的所有文件路径列表，检查是否有文件
            file_paths = get_file_paths(path_zip)
            if not file_paths:
                logger.warning(LANG["main_no_file_warning"].format("#" * 6, path_zip, "#" * 6))
                ui_display_msg(self.root, LANG["main_no_file_warning_msg"].format(path_zip), 'warning')
                return

            # 对文件路径列表按解压目标进行初步分组
            path_groups = group_file_paths(file_paths)

            # 生成全文件分组列表，获取空闲磁盘，看条件替换目标目录
            full_infos = group_list_by_lens(path_groups)
            disk_free = psutil.disk_usage(Path(path_zip).anchor).free
            path_dest = self.entry_dest.get().strip()
            if path_dest:
                path_dest = Path(path_dest)
                try:
                    path_dest.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(LANG["main_path_dest_error"].format("#" * 6, path_dest, e))
                    ui_display_msg(self.root, LANG["main_path_dest_error_msg"].format(path_dest), 'error')
                    return
                full_infos = [{**file_info, 'target_path': str(path_dest / Path(*Path(file_info['target_path']).parts[len(Path(path_zip).parts):]))} for file_info in full_infos]
                disk_free = psutil.disk_usage(Path(path_dest).anchor).free

            # 筛选出压缩文件分组列表，检查是否有压缩文件
            is_force = self.var_sfrc.get()
            file_infos = group_files_main(full_infos, path_zip, path_dest, is_force)
            if not file_infos:
                logger.warning(LANG["main_no_file_infos_warning"].format("#" * 6, path_zip, "#" * 6))
                ui_display_msg(self.root, LANG["main_no_file_infos_warning_msg"].format(path_zip), 'warning')
                return

            # 计算变量
            file_size = sum(get_target_size(p) for i in file_infos for p in i['file_list'])
            file_size_format = format_size(file_size)
            file_in_total_number = len(file_infos)
            failed_counts = 0
            finished_counts = 0
            is_delete = self.var_sdlt.get()
            self.bottom_run.configure(maximum=file_in_total_number)

            # 磁盘剩余空间低警告
            no_warnning = self.var_warn.get()
            if disk_free < file_size and not no_warnning:
                ui_display_msg(self.root, LANG["disk_free_warning"], 'warning')
                return

            # CPU 负载高警告
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > CPU_LIMIT and not no_warnning:
                ui_display_msg(self.root, LANG["cpu_usage_warning"], 'warning')
                return

            # 内存使用率高警告
            memory_usage = psutil.virtual_memory().percent
            if memory_usage > MEMORY_LIMIT and not no_warnning:
                ui_display_msg(self.root, LANG["memory_usage_warning"], 'warning')
                return

            # 解压后操作
            def post_action(result):
                nonlocal failed_counts
                nonlocal finished_counts
                return_code = result['code']
                main_file = result['file_info']['main_file']

                # 错误代码
                ERROR_CODE = {
                    -1: LANG["unzip_run_failed"].format(main_file),
                    0: LANG["unzip_success"].format(main_file),
                    1: LANG["unzip_failed1"].format(main_file),
                    2: LANG["unzip_failed2"].format(main_file),
                    3: LANG["unzip_failed3"].format(main_file),
                    4: LANG["unzip_failed4"].format(main_file),
                    5: LANG["unzip_failed5"].format(main_file),
                    6: LANG["unzip_failed6"].format(main_file),
                    7: LANG["unzip_failed7"].format(main_file),
                    8: LANG["unzip_failed8"].format(main_file),
                    9: LANG["unzip_failed9"].format(main_file),
                    10: LANG["unzip_failed10"].format(main_file),
                }

                if return_code == 0:
                    del_list = [remove_target(file_del) for file_del in result['file_info']['file_list']] if is_delete == 1 else None
                    finished_counts += 1
                    self.text_logs.insert(END, ERROR_CODE[return_code] + '\n', "green")
                else:
                    del_list = [remove_target(result['file_info']['target_path'])]
                    failed_counts += 1
                    self.text_logs.insert(END, ERROR_CODE[return_code] + '\n', "red")
                logger.debug(LANG["extra_debug_del_list"].format(list_to_str(del_list)))
                self.update_progress(file_in_total_number, var_prog)

            # 多进程解压
            start_time = time.time()
            password_list = read_file_to_list(self.entry_pass.get()) if Path(self.entry_pass.get()).is_file() else [self.entry_pass.get()]
            password_list = set(password_list) if password_list else ()
            parallel = min(file_in_total_number, int(self.var_para.get()), round(cpu_count() / 2) if cpu_count() > 3 else 1)

            with Pool(processes=parallel) as self.process_pool:
                for file_info in file_infos:
                    self.process_pool.apply_async(file_unzip, args=(file_info, password_list), callback=post_action)
                self.process_pool.close()
                self.process_pool.join()

            elapsed_time = round(time.time() - start_time, 2)
            your_speed = calculate_transfer_speed(file_size, elapsed_time)
            logger.info(LANG["main_info_done"].format('#' * 6, '#' * 6, file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time, your_speed))
            ui_display_msg(self.root, LANG["main_info_done_msg"].format(file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time, your_speed), 'info')

        # 故障处理
        except Exception as e:
            logger.error(LANG["main_error"].format('#' * 6, '#' * 6, e))
            ui_display_msg(self.root, LANG["main_error_msg"], 'error')

        # 恢复按钮状态
        finally:
            self.bottom_run = ttk.Button(self.frame_bottom, text=LANG["bottom_run_text"], image=self.img_run, bootstyle="danger", command=lambda: thread_it(self.main, ))
            self.bottom_run.config(compound=LEFT) if self.var_mini.get() else NONE
            self.bottom_run.grid(row=0, column=6, sticky='WE')

    # 启动Tkinter
    def run(self):
        self.root.mainloop()

    def on_closing(self):
        if self.process_pool is not None:
            self.process_pool.terminate()
            self.process_pool.join()
        self.root.destroy()


if __name__ == '__main__':
    freeze_support()
    set_priority()

    app = BrutalityExtractor()
    app.run()
