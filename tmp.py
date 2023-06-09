# import webbrowser
# import time
# import os.path
# import requests
# from multiprocessing import Pool, cpu_count
# from threading import Thread, Lock
# import psutil
#
# import ttkbootstrap as ttk
# import tkinter as tk
# from ttkbootstrap.constants import *
# from ttkbootstrap.dialogs import Messagebox
# from tkinter import filedialog
#
# from modules.log_conf import configure_logging
# from modules.file_unzip import unzip
# from modules.file_ops import *
# from modules.math_until import *
#
# CONFIG_LIST = read_txt_to_list(r'config/config.ini')
#
# logger = configure_logging(console_output=True,
#                            log_level=CONFIG_LIST[10] if len(CONFIG_LIST) > 10 and CONFIG_LIST[10] in ['ERROR', 'WARNING', 'INFO', 'DEBUG'] else 'INFO',
#                            max_log_size=int(CONFIG_LIST[11]) if len(CONFIG_LIST) > 11 and CONFIG_LIST[11].isdigit() else 10,
#                            backup_count=int(CONFIG_LIST[12]) if len(CONFIG_LIST) > 12 and CONFIG_LIST[12].isdigit() else 7,
#                            )
#
# # 图标
# ICO = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUVFFwtLSxslTk4aRE1NGl9OThluTk4Zb05OGmFNTRhIUFAYKU5OEw0AAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVVUAA01NHCRNTRlsS0sZtktLGOFLSxn0S0sZ/EtLGf5LSxn+S0sZ/EtLGPZMTBnkS0sZvU1NGXdNTRcrMzMzBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUhIGxxMTBh8S0sY2UpKGftKShn/SkoZ/0pKGf9KShn/SkoZ/0pKGf9KShn/SkoZ/0pKGf9KShn/SUkZ/ElJGeBJSRmKTU0cJAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8/AARJSRlFSEgYxEhIGPtISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0dHGP1HRxjRSEgYVFVVKgYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABVVSoGRkYXYUhIGORbWy3/V1cp/0dHGP9GRhj/RkYX/0ZGF/9GRhf/SUkb/2BgM/96elL/hIRc/3Z2Tf9ZWSv/R0cY/0ZGF/9GRhf/RkYX/0ZGF/9GRhbsRkYYdExMGQoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPz8ABEVFF2NFRRfseXlR/97ez//Hx7H/UVEj/0REF/9ERBf/REQX/1hYLP+oqIv/5ubb//j49P/8/Pj/9vbx/9zczv+NjWn/Skod/0NDFv9DQxb/Q0MW/0REF/9LSx3zXV0weJ+ffwgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCQhhJQUEW5lZWKv/W1sb//////9PTwv9OTiP/QUEW/0FBFv9ZWS//x8e0//z8+//7+/n/6+vj/+jo3//39/P///////X18P+Wlnb/REQZ/0REGf9paUL/p6eK/8zMuv/e3tHv9vbxX////wIAAAAAAAAAAAAAAAAAAAAAPT0XIT8/Fco/PxX/jY1s//v7+P/4+PT/hoZl/z8/Fv8+PhX/RkYc/7S0m//9/fz/7Ozk/5SUdP9dXTb/WFgx/35+W//c3M7////+/+3t5f92dlD/mJh5/+vr4//+/v7////////////+/v7b////MAAAAAAAAAAAAAAAADMzAAU+PhSHOzsU/EZGHv/Ly7n//////9HRwf9KSiL/PDwU/zw8FP9paUT/8PDq//r69v+NjW7/Pj4W/zs7FP87OxT/PDwU/21tSf/s7OT////+/+jo3f/39/P////+/+/v6f/Kyrj/srKc/76+qv7V1cWgsrKyCgAAAAAAAAAAPj4WLTo6E+A5ORP/W1s2/+zs5P/9/fz/lJR3/zk5E/85ORP/OTkT/5WVeP/+/v3/39/T/05OKf84OBP/ODgT/zg4E/84OBP/PDwW/6ioj//+/v3///////7+/v/V1cf/a2tJ/0FBG/85ORT/PT0X/0tLJe1HRx9AAAAAAAAAAAI3NxJ9NjYS/TY2Ev9wcE//+Pj1//X18P9nZ0X/NjYS/zY2Ev83NxP/rKyV///////GxrX/PDwY/zU1Ev81NRL/NTUS/zU1Ev81NRL/Z2dH//T08P//////5+fe/2FhQP81NRL/NTUS/zU1Ev81NRL/NDQR/jU1EpgzMwAFODgOEjMzEMUzMxH/MzMR/319YP/8/Pr/6urj/1NTMf8zMxH/MzMR/zQ0Ev+pqZL//////8vLvP88PBn/MzMR/zMzEf8yMhH/MjIR/zIyEf9lZUX/9fXw///////W1sr/QkIg/zIyEf8yMhH/MjIR/zIyEf8yMhH/MjIQ2DMzER4yMg8zMDAQ6zAwEP8wMBD/f39l//39/P/m5t7/S0ss/zAwEP8wMBD/MDAQ/4+Pdv/+/v3/5+fe/1FRMf8wMBD/MDAQ/zAwEP8vLxD/MDAQ/4uLcP/9/fz//////+/v6P9YWDn/Ly8Q/y8vEP8vLxD/Ly8Q/y8vEP8uLg/1MTERSDAwEVktLQ/6Li4P/y4uD/92dlr/+/v5/+rq4/9PTzD/Li4P/y0tD/8tLQ//ZGRG//T07//9/fv/np6H/zMzFP8tLQ//LS0P/y0tD/9BQSL/zc2/////////////+vr3/29vU/8tLQ//LCwP/ywsD/8sLA//LCwP/ywsD/4tLQ91LCwOeSsrDv4rKw7/KysO/2RkSP/39/P/8vLt/1paPf8rKw7/KysO/ysrDv85ORv/x8e3///////y8u3/i4ty/zs7Hf8xMRP/REQm/6mplf/7+/n/8/Ps//n59v/9/fz/gYFo/yoqDv8qKg7/KioO/yoqDv8qKg7/KioO/ysrD5gpKQ6MKSkO/ykpDv8pKQ7/Tk4y/+zs5f/6+vj/cnJY/ykpDv8pKQ7/KSkO/ykpDv9nZ03/7e3n///////39/T/0dHE/8DAr//a2s///Pz6//j49v+ioon/6Ojh/////v+Li3H/KCgN/ygoDf8oKA3/KCgN/ygoDf8oKA3/KSkNrCkpDo4nJw3/JycN/ycnDf84OB3/1NTJ/////v+cnIf/KCgO/ycnDf8mJg3/JiYN/ysrEf+Cgmr/7u7o///////////////////////7+/n/r6+e/1ZWOv/p6eL//v79/4iIb/8mJg3/JiYN/yYmDf8mJg3/JiYN/yYmDf8nJw2uJycNgSUlDP8lJQz/JSUM/ykpD/+qqpf//////83NwP80NBn/JSUM/yUlDP8lJQz/JSUM/yoqEP9jY0r/ubmp/+Dg1//l5d7/09PI/5KSff84OB7/UFA2/+/v6v/9/fz/e3tl/yUlDP8lJQz/JSUM/yUlDP8lJQz/JSUM/yYmDKElJQxmJCQM/CUlDP8lJQz/JCQM/25uVv/5+fb/8fHs/1tbQv8kJAz/JCQM/yQkDP8kJAz/JCQM/yUlDP8sLBP/PT0k/0FBKP81NRz/JycO/yQkDP9gYEf/9/fz//r6+P9ra1P/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JiYNhCcnC0EkJAzzJCQM/yQkDP8kJAz/PT0k/9vb0f/+/v7/pqaU/ykpEP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/3p6Y//9/fv/8vLu/1ZWPf8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDPooKAtZIyMRHSQkC9ckJAz/JCQM/yQkDP8nJw7/l5eD//39/P/p6eL/UlI5/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8lJQ3/n5+M///////h4dn/Pz8m/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM5icnCy0zMwAFJSUNnCQkDP8kJAz/JCQM/yQkDP9KSjD/4+Pa//7+/v+wsJ//Li4V/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/y8vFv/Hx7n//////8HBs/8tLRP/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAy1KioVDAAAAAAmJg5IIyML8SQkDP8kJAz/JCQM/ycnDv+Ojnn/+/v5//X18f94eGH/JiYO/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/S0sy/+np4//+/v3/jY14/yUlDP8kJAz/JCQM/yQkDP8kJAz/IyMM+CQkDWEAAAAAAAAAACQkEg4lJQ2wJCQM/yQkDP8kJAz/JCQM/zk5H//Gxrj////+/+Pj2v9ZWUD/JSUN/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yYmDf+MjHb//f37/+3t5/9TUzr/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAzGKioKGAAAAAAAAAAAAAAAACcnC0EkJAzoJCQM/yQkDP8kJAz/JCQM/1VVPP/g4Nj////+/9XVyf9SUjj/JSUN/yQkDP8kJAz/JCQM/yQkDP8kJAz/RUUs/9vb0v////7/tram/y0tE/8kJAz/JCQM/yQkDP8kJAz/IyML8SYmC1cAAAABAAAAAAAAAAAAAAAAMzMABSUlDHwjIwz4JCQM/yQkDP8kJAz/JiYN/2pqUv/p6eL//v7+/9jYzv9mZk7/KysS/yQkDP8kJAz/JCQM/zo6IP+zs6P//f38/+3t5/9dXUT/JCQM/yQkDP8kJAz/JCQM/yQkDPslJQyUMzMZCgAAAAAAAAAAAAAAAAAAAAAAAAAALS0PESUlDJ4jIwz7JCQM/yQkDP8kJAz/JycP/3BwV//m5t/////+/+/v6f+srJv/bGxU/1xcQv93d1//xsa5//v7+v/5+ff/lZWA/ykpEf8kJAz/JCQM/yQkDP8kJAz9JSUMsicnCRoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKioKGCQkDKEjIwz5JCQM/yQkDP8kJAz/JycO/15eRv/NzcH/+/v5/////v/5+fb/9fXx//v7+f//////9vbz/6Ojj/8zMxn/JCQM/yQkDP8kJAz/JCQM/CQkDLQkJA4jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJiYMFCUlDYgkJAvuJCQM/yQkDP8kJAz/JSUM/zs7Iv+Hh3L/zs7C/+zs5f/y8u7/6urk/8rKvv95eWL/Ly8W/yQkDP8kJAz/JCQM/yQkDPQmJg2ZLS0JHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHx8ACCUlDFEkJA3DIyMM+CQkDP8kJAz/JCQM/yUlDf80NBr/S0sy/1RUPP9JSTD/MjIZ/yUlDf8kJAz/JCQM/yMjDPolJQzOJSUNYCoqFQwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASwsCxcmJgxjJCQMuyQkC+skJAz8JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/SQkC+8kJAvDJCQLbyoqER4AAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEkJBIOJiYONSYmDGkmJg2ZJCQMuyUlDMwlJQzNJSUMviUlDJ4nJw1vJiYMOyoqDhIAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/8AD//8AAP/8AAA/+AAAH/AAAA/gAAAHwAAAA8AAAAOAAAABgAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAGAAAABwAAAAcAAAAPgAAAH8AAAD/gAAB/8AAA//gAAf/+AAf8='
# IMAGE_FILES = {
#     'Play': 'icons8_Play_16.png',
#     'Wait': 'icons8_Wait_16.png',
#     'GitHub': 'icons8_GitHub_16.png',
#     'Available_Updates': 'icons8_Available_Updates_16.png',
#     'Bulleted_List': 'icons8_Bulleted_List_16.png',
#
# }
#
# lock = Lock()
#
#
# def thread_it(func, *args, daemon=True, name=None):
#     """
#     多线程运行
#
#     :param func: 函数名
#     :param daemon: 后台线程
#     :param name: 新线程名字
#
#     """
#
#     # noinspection PyShadowingNames
#     def wrapper(*args):
#         try:
#             func(*args)
#         except Exception as e:
#             logger.error(f"线程发生错误 {name}: {e}")
#
#     t = Thread(target=wrapper, args=args, daemon=daemon, name=name)
#     t.start()
#
#
# class ToolTip:
#     def __init__(self, widget, text):
#         self.widget = widget
#         self.text = text
#         self.tooltip_window = None
#         self.widget.bind("<Enter>", self.show_tooltip)
#         self.widget.bind("<Leave>", self.hide_tooltip)
#
#     def show_tooltip(self, event=None):
#         x, y, _, _ = self.widget.bbox("insert")
#         x += self.widget.winfo_rootx() + 35
#         y += self.widget.winfo_rooty() + 35
#
#         self.tooltip_window = ttk.Toplevel(self.widget)
#         self.tooltip_window.wm_overrideredirect(True)
#         self.tooltip_window.wm_geometry(f"+{x}+{y}")
#
#         label = ttk.Label(self.tooltip_window, text=self.text, background="#fffff0", relief="solid", borderwidth=1)
#         label.pack()
#
#     def hide_tooltip(self, event=None):
#         if self.tooltip_window:
#             self.tooltip_window.destroy()
#             self.tooltip_window = None
#
#
# class BrutalityExtractor:
#     """
#     软件名：BrutalityExtractor\n
#     版本：1.0\n
#     更新时间：2023.05.30\n
#     打包命令：pyinstaller -F -w -i BEUI.ico BrutalityExtractor.py\n
#     TK 文档：https://docs.python.org/zh-cn/3.10/library/tk.html
#     UI 文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/
#     """
#
#     def __init__(self):
#         # 主窗口配置
#         self.root = ttk.Window()
#         self.style = ttk.Style(theme='yeti')
#         self.root.title("BrutalityExtractor 1.0.0")
#         self.root.attributes("-alpha", 1)
#         self.root.geometry('640x800')
#         self.root.place_window_center()
#         self.root.minsize(538, 800)
#         self.root.iconbitmap(create_temp_icon_file(ICO, logger))
#         self.root.grid_columnconfigure(0, weight=1)
#         self.root.grid_rowconfigure(10, weight=1)
#
#         # 定义回调
#         self.digit_func = self.root.register(is_numeric)
#         self.alpha_func = self.root.register(is_alpha)
#         self.empty_func = self.root.register(is_not_empty)
#
#         # 定义图标
#         self.photoimages = []
#         imgpath = Path(__file__).parent / 'media'
#         for key, val in IMAGE_FILES.items():
#             _path = imgpath / val
#             try:
#                 self.photoimages.append(ttk.PhotoImage(name=key, file=_path))
#             except Exception as e:
#                 logger.error(f'图标文件：{_path} 丢失。{e}')
#                 self.photoimages.append(ttk.PhotoImage(name=key, file=''))
#
#         # 定义事件
#         def on_entry_click(event, entry, placeholder_text):
#             if entry.get() == placeholder_text:
#                 entry.delete(0, END)
#                 entry.configure(foreground='black')
#
#         def on_focus_out(event, entry, placeholder_text):
#             if entry.get() == "":
#                 entry.insert(0, placeholder_text)
#                 entry.configure(foreground='grey')
#
#         # 更新输入框
#         def update_entry(entry, config_value, placeholder):
#             if config_value:
#                 entry.insert(0, config_value)
#                 entry.configure(foreground='black')
#             else:
#                 entry.insert(0, placeholder)
#                 entry.configure(foreground='grey')
#
#         # 文件选择对话框
#         def select_file(entry):
#             file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("INI files", "*.ini"), ("CSV files", "*.csv"), ("All files", "*.*")))
#             if file_path:
#                 entry.delete(0, END)
#                 entry.insert(0, file_path)
#                 entry.configure(foreground='black')
#
#         def select_directory(entry):
#             dir_path = filedialog.askdirectory()
#             if dir_path:
#                 entry.delete(0, END)
#                 entry.insert(0, dir_path)
#                 entry.configure(foreground='black')
#
#         # 日志等级选择菜单样式更改
#         def update_logl_style(*args):
#             selected_option = self.var_logl.get()
#             if selected_option == 'ERROR':
#                 self.menubutton_logl.config(bootstyle="danger-outline")
#             elif selected_option == 'WARNING':
#                 self.menubutton_logl.config(bootstyle="warning-outline")
#             elif selected_option == 'INFO':
#                 self.menubutton_logl.config(bootstyle="info-outline")
#             else:
#                 self.menubutton_logl.config(bootstyle="dark-outline")
#
#         # 基础配置区块
#         self.labelframe_basic = ttk.LabelFrame(self.root, text="基础配置")
#         self.labelframe_basic.grid(row=0, column=0, sticky=W + E, padx=(0, 0), pady=(5, 15))
#         self.labelframe_basic.columnconfigure(0, weight=1)
#
#         # 解压目录相关元素
#         self.label_path = ttk.Label(self.labelframe_basic, text='解压目录：')
#         self.label_path.grid(row=1, column=0, sticky=W, padx=(15, 0), pady=(4, 0))
#
#         self.entry_path = ttk.Entry(self.labelframe_basic, bootstyle="dark", validate="focus", validatecommand=(self.empty_func, '%P'))
#         self.entry_path.grid(row=1, column=0, sticky=W + E, padx=(88, 88), pady=(4, 0))
#         self.entry_path.bind('<FocusIn>', lambda event: on_entry_click(event, self.entry_path, self.entry_path_placeholder))
#         self.entry_path.bind('<FocusOut>', lambda event: on_focus_out(event, self.entry_path, self.entry_path_placeholder))
#
#         self.bottom_path = ttk.Button(self.labelframe_basic, text='浏览...', width=6, bootstyle="secondary-outline", command=lambda: select_directory(self.entry_path))
#         self.bottom_path.grid(row=1, padx=(6, 15), pady=(4, 0), sticky=E)
#
#         self.entry_path_placeholder = r"压缩文件存放路径，目录内别放无关文件。"
#         update_entry(self.entry_path, CONFIG_LIST[0] if len(CONFIG_LIST) > 0 else '', self.entry_path_placeholder)
#         ToolTip(self.bottom_path, "手动选择解压目录")
#
#         # 目标目录相关元素
#         self.label_dest = ttk.Label(self.labelframe_basic, text='目标目录：')
#         self.label_dest.grid(row=2, column=0, sticky=W, padx=(15, 0), pady=(14, 0))
#
#         self.entry_dest = ttk.Entry(self.labelframe_basic, validate="focus")
#         self.entry_dest.grid(row=2, column=0, sticky=W + E, padx=(88, 88), pady=(14, 0))
#         self.entry_dest.bind('<FocusIn>', lambda event: on_entry_click(event, self.entry_dest, self.entry_dest_placeholder))
#         self.entry_dest.bind('<FocusOut>', lambda event: on_focus_out(event, self.entry_dest, self.entry_dest_placeholder))
#
#         self.bottom_dest = ttk.Button(self.labelframe_basic, text='浏览...', width=6, bootstyle="secondary-outline", command=lambda: select_directory(self.entry_dest))
#         self.bottom_dest.grid(row=2, padx=(6, 15), pady=(14, 0), sticky=E)
#
#         self.entry_dest_placeholder = r"解压文件存放路径，不填则在解压目录就地解压。"
#         update_entry(self.entry_dest, CONFIG_LIST[1] if len(CONFIG_LIST) > 1 else '', self.entry_dest_placeholder)
#         ToolTip(self.bottom_dest, "手动选择目标目录")
#
#         # 密码输入相关元素
#         self.label_pass = ttk.Label(self.labelframe_basic, text='解压密码：')
#         self.label_pass.grid(row=3, column=0, sticky=W, padx=(15, 0), pady=(14, 14))
#
#         self.entry_pass = ttk.Entry(self.labelframe_basic, validate="focus", validatecommand=('', '%P'))
#         self.entry_pass.grid(row=3, column=0, sticky=W + E, padx=(88, 88), pady=(14, 14))
#         self.entry_pass.bind('<FocusIn>', lambda event: on_entry_click(event, self.entry_pass, self.entry_pass_placeholder))
#         self.entry_pass.bind('<FocusOut>', lambda event: on_focus_out(event, self.entry_pass, self.entry_pass_placeholder))
#
#         self.bottom_pass = ttk.Button(self.labelframe_basic, text='选择...', width=6, bootstyle="secondary-outline", command=lambda: select_file(self.entry_pass))
#         self.bottom_pass.grid(row=3, padx=(6, 15), pady=(14, 14), sticky=E)
#
#         self.entry_pass_placeholder = r"不填为空。输入单个密码或密码文本（一行一个），例如：Abc12# 或 D:\pass.txt"
#         update_entry(self.entry_pass, CONFIG_LIST[2] if len(CONFIG_LIST) > 2 else '', self.entry_pass_placeholder)
#         ToolTip(self.bottom_pass, "手动选择密码文件")
#
#         # 高级配置区块
#         self.labelframe_advance = ttk.LabelFrame(self.root, text="高级配置")
#         self.labelframe_advance.grid(row=4, column=0, sticky=W + E, padx=(0, 0), pady=(0, 15))
#         self.labelframe_advance.columnconfigure(0, weight=1)
#
#         # 进程数量相关元素
#         self.label_para = ttk.Label(self.labelframe_advance, text='进程数量：')
#         self.label_para.grid(row=5, column=0, sticky=W, padx=(15, 0), pady=(4, 0))
#
#         self.spinbox_para = ttk.Spinbox(self.labelframe_advance, from_=1, to=round(cpu_count() / 2) if cpu_count() > 3 else 1, increment=1, width=3, state="readonly")
#         self.spinbox_para.grid(row=5, column=0, sticky=W, padx=(88, 0), pady=(4, 0))
#
#         self.spinbox_para.set(CONFIG_LIST[3] if len(CONFIG_LIST) > 3 else '1')
#         ToolTip(self.label_para, "同时运行解压进程数量，最高不超过 CPU 支持线程数的一半")
#
#         # 排除目录相关元素
#         self.label_xcld = ttk.Label(self.labelframe_advance, text='排除目录：')
#         self.label_xcld.grid(row=7, column=0, sticky=W, padx=(15, 0), pady=(14, 0))
#
#         self.entry_xcld = ttk.Entry(self.labelframe_advance, validate="focus", validatecommand=('', '%P'))
#         self.entry_xcld.grid(row=7, column=0, sticky=W + E, padx=(88, 88), pady=(14, 0))
#         self.entry_xcld.bind('<FocusIn>', lambda event: on_entry_click(event, self.entry_xcld, self.entry_xcld_placeholder))
#         self.entry_xcld.bind('<FocusOut>', lambda event: on_focus_out(event, self.entry_xcld, self.entry_xcld_placeholder))
#
#         self.bottom_xcld = ttk.Button(self.labelframe_advance, text='选择...', width=6, bootstyle="secondary-outline", command=lambda: select_file(self.entry_xcld))
#         self.bottom_xcld.grid(row=7, padx=(6, 15), pady=(14, 0), sticky=E)
#
#         self.entry_xcld_placeholder = r"要删除的目录，留空不开启。输入单个目录名或目录名文本，支持通配符。"
#         update_entry(self.entry_xcld, CONFIG_LIST[4] if len(CONFIG_LIST) > 4 else '', self.entry_xcld_placeholder)
#         ToolTip(self.bottom_xcld, "手动选择目录名列表")
#
#         # 排除文件相关元素
#         self.label_xclf = ttk.Label(self.labelframe_advance, text='排除文件：')
#         self.label_xclf.grid(row=8, column=0, sticky=W, padx=(15, 0), pady=(14, 0))
#
#         self.entry_xclf = ttk.Entry(self.labelframe_advance, validate="focus", validatecommand=('', '%P'))
#         self.entry_xclf.grid(row=8, column=0, sticky=W + E, padx=(88, 88), pady=(14, 0))
#         self.entry_xclf.bind('<FocusIn>', lambda event: on_entry_click(event, self.entry_xclf, self.entry_xclf_placeholder))
#         self.entry_xclf.bind('<FocusOut>', lambda event: on_focus_out(event, self.entry_xclf, self.entry_xclf_placeholder))
#
#         self.bottom_xclf = ttk.Button(self.labelframe_advance, text='选择...', width=6, bootstyle="secondary-outline", command=lambda: select_file(self.entry_xclf))
#         self.bottom_xclf.grid(row=8, padx=(6, 15), pady=(14, 0), sticky=E)
#
#         self.entry_xclf_placeholder = r"要删除的文件，留空不开启。输入单个文件名或文件名文本，支持通配符。"
#         update_entry(self.entry_xclf, CONFIG_LIST[5] if len(CONFIG_LIST) > 5 else '', self.entry_xclf_placeholder)
#         ToolTip(self.bottom_xclf, "手动选择文件名列表")
#
#         # 附加功能相关元素
#         self.label_extr = ttk.Label(self.labelframe_advance, text='附加功能：')
#         self.label_extr.grid(row=9, column=0, sticky=W, padx=(15, 0), pady=(14, 0))
#
#         self.var_extr = ttk.IntVar()
#         self.checkbutton_extr = ttk.Checkbutton(self.labelframe_advance, variable=self.var_extr, onvalue=1, offvalue=0, bootstyle="danger-square-toggle")
#         self.checkbutton_extr.grid(row=9, column=0, sticky=W + E, padx=(88, 0), pady=(14, 0))
#
#         self.var_extr.set(1 if len(CONFIG_LIST) > 6 and CONFIG_LIST[6] != '0' else 0)
#         ToolTip(self.label_extr, "附加功能开关。开启后关闭解压功能，对目标目录执行：删除排除文件、消除冗余目录、清理空目录功能")
#
#         # 释放空间相关元素
#         self.label_sdlt = ttk.Label(self.labelframe_advance, text='释放空间：')
#         self.label_sdlt.grid(row=6, column=0, sticky=W, padx=(140, 0), pady=(14, 0))
#
#         self.var_sdlt = ttk.IntVar()
#         self.checkbutton_sdlt = ttk.Checkbutton(self.labelframe_advance, variable=self.var_sdlt, onvalue=1, offvalue=0, bootstyle="success-square-toggle")
#         self.checkbutton_sdlt.grid(row=6, column=0, sticky=W + E, padx=(213, 0), pady=(14, 0))
#
#         self.var_sdlt.set(1 if len(CONFIG_LIST) > 7 and CONFIG_LIST[7] != '0' else 0)
#         ToolTip(self.label_sdlt, "解压成功后，立即删除原始压缩包文件")
#
#         # 消除冗余相关元素
#         self.label_rddd = ttk.Label(self.labelframe_advance, text='消除冗余：')
#         self.label_rddd.grid(row=9, column=0, sticky=W, padx=(140, 0), pady=(14, 0))
#
#         self.var_rddd = ttk.IntVar()
#         self.checkbutton_rddd = ttk.Checkbutton(self.labelframe_advance, variable=self.var_rddd, onvalue=1, offvalue=0, bootstyle="success-square-toggle")
#         self.checkbutton_rddd.grid(row=9, column=0, sticky=W + E, padx=(213, 0), pady=(14, 0))
#
#         self.var_rddd.set(1 if len(CONFIG_LIST) > 8 and CONFIG_LIST[8] != '0' else 0)
#         ToolTip(self.label_rddd, "消除冗余目录结构。例如将 D:/zip/zip/zip/ 中的文件提取到 D:/zip/")
#
#         # 清理目录相关元素
#         self.label_mpty = ttk.Label(self.labelframe_advance, text='清理目录：')
#         self.label_mpty.grid(row=9, column=0, sticky=W, padx=(270, 0), pady=(14, 0))
#
#         self.var_mpty = ttk.IntVar()
#         self.checkbutton_mpty = ttk.Checkbutton(self.labelframe_advance, variable=self.var_mpty, onvalue=1, offvalue=0, bootstyle="success-square-toggle")
#         self.checkbutton_mpty.grid(row=9, column=0, sticky=W + E, padx=(343, 0), pady=(14, 0))
#
#         self.var_mpty.set(1 if len(CONFIG_LIST) > 9 and CONFIG_LIST[9] != '0' else 0)
#         ToolTip(self.label_mpty, "清理空目录，谨慎使用")
#
#         # 日志等级相关元素
#         self.label_logl = ttk.Label(self.labelframe_advance, text='日志等级：')
#         self.label_logl.grid(row=10, column=0, sticky=W, padx=(15, 0), pady=(14, 14))
#
#         self.var_logl = ttk.StringVar()
#         self.var_logl.trace_add('write', update_logl_style)
#         self.menubutton_logl = ttk.Menubutton(self.labelframe_advance, text='选项', textvariable=self.var_logl, width=9, bootstyle="default-outline")
#         self.menubutton_logl.grid(row=10, column=0, sticky=W, padx=(88, 0), pady=(14, 14))
#         self.menu_logl = ttk.Menu(self.menubutton_logl, tearoff=False)
#         self.menubutton_logl['menu'] = self.menu_logl
#         self.menu_logl.add_radiobutton(label='ERROR', value='ERROR', variable=self.var_logl)
#         self.menu_logl.add_radiobutton(label='WARNING', value='WARNING', variable=self.var_logl)
#         self.menu_logl.add_radiobutton(label='INFO', value='INFO', variable=self.var_logl)
#         self.menu_logl.add_radiobutton(label='DEBUG', value='DEBUG', variable=self.var_logl)
#
#         self.var_logl.set(CONFIG_LIST[10] if len(CONFIG_LIST) > 10 else 'INFO')
#         ToolTip(self.label_logl, "控制写入日志文件中日志的等级。日志相关选项修改后，要重启程序才能生效")
#
#         # 日志大小相关元素
#         self.label_logs = ttk.Label(self.labelframe_advance, text='日志大小：')
#         self.label_logs.grid(row=10, column=0, sticky=W, padx=(220, 0), pady=(14, 14))
#
#         self.spinbox_logs = ttk.Spinbox(self.labelframe_advance, from_=1, to=10, increment=1, width=2, state="readonly")
#         self.spinbox_logs.grid(row=10, column=0, sticky=W, padx=(293, 0), pady=(14, 14))
#
#         self.spinbox_logs.set(CONFIG_LIST[11] if len(CONFIG_LIST) > 11 else '10')
#         ToolTip(self.label_logs, "单位 MB")
#
#         # 日志数量相关元素
#         self.label_logc = ttk.Label(self.labelframe_advance, text='日志数量：')
#         self.label_logc.grid(row=10, column=0, sticky=W, padx=(370, 0), pady=(14, 14))
#
#         self.spinbox_logc = ttk.Spinbox(self.labelframe_advance, from_=1, to=99, increment=1, width=2, state="readonly")
#         self.spinbox_logc.grid(row=10, column=0, sticky=W, padx=(443, 0), pady=(14, 14))
#
#         self.spinbox_logc.set(CONFIG_LIST[12] if len(CONFIG_LIST) > 12 else '7')
#         ToolTip(self.label_logc, "硬盘中保留日志文件的数量")
#
#         # 忽略警告相关元素
#         self.label_warn = ttk.Label(self.labelframe_advance, text='忽略警告：')
#         self.label_warn.grid(row=6, column=0, sticky=W, padx=(15, 0), pady=(14, 0))
#
#         self.var_warn = ttk.IntVar()
#         self.checkbutton_warn = ttk.Checkbutton(self.labelframe_advance, variable=self.var_warn, onvalue=1, offvalue=0, bootstyle="warning-square-toggle")
#         self.checkbutton_warn.grid(row=6, column=0, sticky=W, padx=(88, 0), pady=(14, 0))
#
#         self.var_warn.set(1 if len(CONFIG_LIST) > 13 and CONFIG_LIST[13] != '0' else 0)
#         ToolTip(self.label_warn, "解压开始前会检测硬件信息，如果资源不足会拒绝运行。打开来关闭检测")
#
#         # 开始运行按钮
#         self.bottom_run = ttk.Button(self.root, text='开始运行', image='Play', compound=LEFT, width=8, bootstyle="danger-outline", command=lambda: thread_it(self.main, ))
#         self.bottom_run.grid(row=9, sticky=E, padx=(6, 15), pady=(0, 0))
#         ToolTip(self.bottom_run, "开始后无法暂停，只能关闭来停止")
#
#         # 项目主页相关元素
#         self.bottom_github = ttk.Button(self.root, text='项目主页', image='GitHub', width=8, bootstyle="light-link", cursor='heart',
#                                         command=lambda: webbrowser.open("https://github.com/hxz393/BrutalityExtractor", new=0))
#         self.bottom_github.grid(row=9, sticky=W, padx=(15, 0), pady=(0, 0))
#         ToolTip(self.bottom_github, "项目主页")
#
#         # 检查更新相关元素
#         self.bottom_update = ttk.Button(self.root, text='检查更新', image='Available_Updates', width=8, bootstyle="light-link", command=lambda: thread_it(self.check_update, ))
#         self.bottom_update.grid(row=9, sticky=W, padx=(55, 0), pady=(0, 0))
#         ToolTip(self.bottom_update, "检查更新")
#
#         # 打开日志相关元素
#         self.bottom_logpath = ttk.Button(self.root, text='打开日志', image='Bulleted_List', width=8, bootstyle="light-link", command=lambda: os.startfile('logs'))
#         self.bottom_logpath.grid(row=9, sticky=W, padx=(95, 0), pady=(0, 0))
#         ToolTip(self.bottom_logpath, "打开日志")
#
#         # 日志文本框相关元素
#         self.text_logs = ttk.Text(self.root, wrap=NONE)
#         self.text_logs.grid(row=10, column=0, sticky=W + E + N + S, padx=(0, 0), pady=(15, 0))
#         self.text_logs.tag_config("red", foreground="#f04124")
#         self.text_logs.tag_config("green", foreground="#43ac6a")
#
#         self.text_logs_scrollbar = ttk.Scrollbar(self.root, bootstyle="light")
#         self.text_logs_scrollbar.grid(row=10, column=0, sticky=S + N + E, rowspan=1, padx=(0, 0), pady=(15, 0))
#         self.text_logs_scrollbar.configure(command=self.text_logs.yview)
#         self.text_logs.configure(yscrollcommand=self.text_logs_scrollbar.set)
#
#         # 状态栏相关元素
#         self.labelframe_stat = ttk.Frame(self.root)
#         self.labelframe_stat.grid(row=11, column=0, sticky=W + E, padx=(15, 1), pady=(15, 15))
#         self.labelframe_stat.columnconfigure(0, weight=1)
#
#         self.label_stat = ttk.Label(self.labelframe_stat, text='状态：')
#         self.label_stat.grid(row=12, column=0, sticky=W, padx=(10, 0), pady=(0, 0))
#
#         # 状态计数
#         self.failed_counts = 0
#         self.finished_counts = 0
#
#     # 检查更新函数
#     def check_update(self):
#         current_version = self.root.title()
#         self.bottom_update['stat'] = 'disabled'
#         url = "https://blog.x2b.net/ver/brutalityextractorversion.txt"
#
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 latest_version = response.text.strip()
#                 if latest_version != current_version:
#                     self.root.after(10, lambda: Messagebox.show_info(
#                         title='提示',
#                         message=f"当前版本：{current_version}\n"
#                                 f"最新版本：{latest_version}\n"
#                                 f"可以到项目主页下载新版"))
#                 elif latest_version == current_version:
#                     self.root.after(10, lambda: Messagebox.show_info(
#                         title='提示',
#                         message=f"当前版本：{current_version}\n"
#                                 f"最新版本：{latest_version}\n"
#                                 f"目前使用的是最新版"))
#             else:
#                 self.root.after(10, lambda: Messagebox.show_info(
#                     title='提示',
#                     message=f"检查更新失败"))
#
#         except Exception as e:
#             logger.error(f"发送网络请求到 {url} 失败：{e}")
#             self.root.after(10, lambda: Messagebox.show_error(
#                 title='错误',
#                 message=f"网络连接失败"))
#
#         finally:
#             self.bottom_update['stat'] = 'normal'
#
#
#     # 主函数
#     def main(self):
#         start_time = time.time()
#
#         self.failed_counts = 0
#         self.finished_counts = 0
#
#         # 切换按钮状态#
#         self.text_logs.delete(1.0, END)
#         self.bottom_run['text'] = '等待'
#         self.bottom_run['image'] = 'Wait'
#         self.bottom_run['stat'] = 'disabled'
#
#         try:
#             # 从输入框获取值
#             path_zip = self.entry_path.get() if self.entry_path.get() != self.entry_path_placeholder else ''
#             path_dest = self.entry_dest.get() if self.entry_dest.get() != self.entry_dest_placeholder else ''
#             password = self.entry_pass.get() if self.entry_pass.get() != self.entry_pass_placeholder else ''
#             parallel = self.spinbox_para.get()
#             xcl_dir = self.entry_xcld.get() if self.entry_xcld.get() != self.entry_xcld_placeholder else ''
#             xcl_file = self.entry_xclf.get() if self.entry_xclf.get() != self.entry_xclf_placeholder else ''
#             is_extra = self.var_extr.get()
#             is_delete = self.var_sdlt.get()
#             is_redundant = self.var_rddd.get()
#             is_empty = self.var_mpty.get()
#             log_level = self.var_logl.get() if self.var_logl.get() in ['ERROR', 'WARNING', 'INFO', 'DEBUG'] else 'INFO'
#             log_size = self.spinbox_logs.get()
#             log_count = self.spinbox_logc.get()
#             no_warnning = self.var_warn.get()
#
#             # 写入到配置
#             config_curr = f'{path_zip}\n{path_dest}\n{password}\n{parallel}\n' \
#                           f'{xcl_dir}\n{xcl_file}\n{is_extra}\n{is_delete}\n{is_redundant}\n' \
#                           f'{is_empty}\n{log_level}\n{log_size}\n{log_count}\n{no_warnning}'
#             write_str_to_txt(r'config/config.ini', config_curr, logger)
#
#             # 转换输入值
#             password_set = set(read_txt_to_list(password, logger) if os.path.isfile(password) else [password])
#             parallel_int = min(int(parallel) if parallel.isdigit() else 1, round(cpu_count() / 2) if cpu_count() > 3 else 1)
#             xcld_set = set(read_txt_to_list(xcl_dir, logger) if os.path.isfile(xcl_dir) else [xcl_dir])
#             xclf_set = set(read_txt_to_list(xcl_file, logger) if os.path.isfile(xcl_file) else [xcl_file])
#
#             # 执行附加功能
#             if is_extra:
#                 if not path_dest:
#                     logger.warning(f'{"#" * 6}无法运行。请输入目标目录{"#" * 6}')
#                     self.root.after(10, lambda: Messagebox.show_warning(
#                         title='提示',
#                         message="请输入目标目录"))
#                     return
#
#                 if xcld_set != {''}:
#                     paths = get_folder_paths(path_dest, logger)
#                     remove_matched(paths, logger, xcld_set)
#                     paths_now = get_folder_paths(path_dest, logger)
#                     del_count = len(paths) - len(paths_now)
#                     self.text_logs.insert(END, f'删除 {path_dest} 下的垃圾目录 {del_count} 个。\n', "green")
#
#                 if xclf_set != {''}:
#                     files = get_file_paths(path_dest, logger)
#                     remove_matched(files, logger, xclf_set)
#                     files_now = get_file_paths(path_dest, logger)
#                     del_count = len(files) - len(files_now)
#                     self.text_logs.insert(END, f'删除 {path_dest} 下的垃圾文件 {del_count} 个。\n', "green")
#
#                 if is_redundant:
#                     paths = get_folder_paths(path_dest, logger)
#                     [remove_redundant(i, logger) for i in get_subdirectories(path_dest, logger)]
#                     paths_now = get_folder_paths(path_dest, logger)
#                     del_count = len(paths) - len(paths_now)
#                     self.text_logs.insert(END, f'删除 {path_dest} 下冗余目录 {del_count} 个。\n', "green")
#
#                 if is_empty:
#                     paths = get_folder_paths(path_dest, logger)
#                     remove_empty_dirs(path_dest, logger)
#                     paths_now = get_folder_paths(path_dest, logger)
#                     del_count = len(paths) - len(paths_now)
#                     self.text_logs.insert(END, f'删除 {path_dest} 下空目录 {del_count} 个。\n', "green")
#                 return
#
#             logger.info(f'{"#" * 6}开始批量解压缩文件{"#" * 6}')
#             # 检查目录
#             if not path_zip:
#                 logger.warning(f'{"#" * 6}无法运行。请输入解压目录{"#" * 6}')
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='提示',
#                     message="请输入解压目录"))
#                 return
#
#             # 获取目标目录下的所有文件路径列表，检查是否有文件
#             file_paths = get_file_paths(path_zip, logger)
#             if not file_paths:
#                 logger.warning(f'{"#" * 6}扫描完毕。目录 {path_zip} 下没有文件{"#" * 6}')
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='提示',
#                     message=f'目录 {path_zip} 下没有文件'))
#                 return
#
#             # 对文件路径列表按解压目标进行初步分组
#             path_groups = group_file_paths(file_paths, logger)
#
#             # 生成全文件分组列表，替换掉目标目录
#             disk_free = psutil.disk_usage(Path(path_zip).anchor).free
#             full_infos = group_list_by_lens(path_groups, logger)
#             if path_dest:
#                 path_dest = Path(path_dest)
#                 try:
#                     path_dest.mkdir(parents=True, exist_ok=True)
#                 except Exception as e:
#                     logger.error(f'{"#" * 6}运行错误。目标目录 {path_dest} 创建失败：{e}')
#                     self.root.after(10, lambda: Messagebox.show_error(
#                         title='错误',
#                         message=f'运行错误，目标目录 {path_dest} 创建失败。目录名请勿包含禁止的特殊字符'))
#                     return
#                 full_infos = [{**file_info, 'target_path': str(path_dest / Path(*Path(file_info['target_path']).parts[len(Path(path_zip).parts):]))} for file_info in full_infos]
#                 disk_free = psutil.disk_usage(Path(path_dest).anchor).free
#
#             # 筛选出压缩文件分组列表，检查是否有压缩文件
#             file_infos = group_files_main(full_infos, logger)
#             if not file_infos:
#                 logger.warning(f'{"#" * 6}扫描完毕。目录 {path_zip} 下没有压缩文件{"#" * 6}')
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='提示',
#                     message=f'目录 {path_zip} 下没有压缩文件'))
#                 return
#
#             # 计算变量
#             file_size = sum(get_target_size(p, logger) for i in file_infos for p in i['file_list'])
#             file_size_format = format_size(file_size)
#             file_in_total_number = len(file_infos)
#
#             # 磁盘空间低警告
#             if disk_free < file_size and not no_warnning:
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='警告',
#                     message=f'目前磁盘剩余空间小于压缩文件大小，继续执行可能导致：\n'
#                             f'系统异常、解压失败、其他程序异常等未知错误\n'
#                             f'打开忽略警告，可以跳过磁盘空间检查'))
#                 return
#
#             # CPU 负载高警告
#             cpu_usage = psutil.cpu_percent(interval=1)
#             if cpu_usage > 50 and not no_warnning:
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='警告',
#                     message=f'目前 CPU 使用率大于 50%，继续执行可能导致：\n'
#                             f'系统卡死、解压失败、其他程序异常等未知错误\n'
#                             f'打开忽略警告，可以跳过 CPU 使用率检查'))
#                 return
#
#             # 内存使用率高警告
#             memory_usage = psutil.virtual_memory().percent
#             if memory_usage > 50 and not no_warnning:
#                 self.root.after(10, lambda: Messagebox.show_warning(
#                     title='警告',
#                     message=f'目前内存使用率大于 50%，继续执行可能导致：\n'
#                             f'系统卡死、解压失败、其他程序异常等未知错误\n'
#                             f'打开忽略警告，可以跳过内存使用率检查'))
#                 return
#
#             # 解压后操作
#             def post_action(result):
#                 return_code = result['code']
#
#                 if return_code == 2:
#                     remove_target(result['file_info']['target_path'], logger)
#                     self.failed_counts += 1
#                     self.text_logs.insert(END, result['std'] + '\n', "red")
#                 elif return_code == 0 and is_delete == 1:
#                     [remove_target(file_del, logger) for file_del in result['file_info']['file_list']]
#                     self.finished_counts += 1
#                     self.text_logs.insert(END, result['std'] + '\n', "green")
#                 elif return_code == 0:
#                     self.finished_counts += 1
#                     self.text_logs.insert(END, result['std'] + '\n', "green")
#
#             # 多进程解压
#             thread_pool = Pool(processes=parallel_int)
#             for file_info in file_infos:
#                 thread_pool.apply_async(unzip, args=(file_info, password_set, logger), callback=post_action)
#             thread_pool.close()
#             thread_pool.join()
#
#             end_time = time.time()
#             elapsed_time = end_time - start_time
#             elapsed_time_format = format_time(end_time - start_time)
#             your_speed = calculate_speed(file_size, elapsed_time)
#
#             logger.info(
#                 f"{'#' * 6}压缩文件总数：{file_in_total_number} 解压失败数量：{self.failed_counts} 解压成功数量：{self.finished_counts} 压缩文件总大小：{file_size_format} 进程数：{parallel_int} 花费时间：{elapsed_time_format} 处理速度：{your_speed}{'#' * 6}")
#             self.root.after(10, lambda: Messagebox.ok(title='完成',
#                                                       message=f"压缩文件总数：{file_in_total_number}\n解压失败数量：{self.failed_counts}\n解压成功数量：{self.finished_counts}\n压缩文件总大小：{file_size_format}\n进程数：{parallel_int}\n花费时间：{elapsed_time_format}\n处理速度：{your_speed}"))
#
#
#
#
#         # 故障处理
#         except Exception as e:
#             logger.error(f"{'#' * 6}运行出错，错误信息如下{'#' * 6}\n{str(e)}")
#             self.root.after(10, lambda: Messagebox.ok(title='完成', message=f"运行出错，请到 Github 反馈:("))
#
#         # 恢复按钮状态
#         finally:
#             self.bottom_run['text'] = '开始运行'
#             self.bottom_run['image'] = 'Play'
#             self.bottom_run['stat'] = 'normal'
#
#     # 启动Tkinter
#     def run(self):
#         self.root.mainloop()
#
#
# if __name__ == '__main__':
#     app = BrutalityExtractor()
#     app.run()


import win32event
import win32api
import winerror
import sys
import time

mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print("Multiple instances are not allowed")
    sys.exit(0)
else:
    while True:
        print("Program is starting")
        time.sleep(11)


