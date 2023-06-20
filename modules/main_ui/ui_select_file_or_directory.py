import logging
import os
import tkinter
from tkinter import filedialog, END

logger = logging.getLogger(__name__)


def ui_select_file_or_directory(entry: tkinter.Entry, var: tkinter.StringVar, mode: str) -> None:
    """
    选择文件或目录，并将其路径显示在指定的 tkinter.Entry 组件上。

    :param entry: tkinter.Entry 对象，用于显示选定的文件或目录路径。
    :type entry: tkinter.Entry
    :param var: tkinter.StringVar 对象，用于保存选定的文件或目录路径。
    :type var: tkinter.StringVar
    :param mode: 选择模式，'file' 表示选择文件，其他值表示选择目录。
    :type mode: str
    :return: None
    :rtype: None
    """
    try:
        if mode == 'file':
            path = filedialog.askopenfilename()
        else:
            path = filedialog.askdirectory()

        if path:
            path = os.path.normpath(path)
            var.set(path)
            entry.delete(0, END)
            entry.insert(0, path)
            entry.configure(foreground='black')
        else:
            logger.warning("No path was selected.")
    except Exception as e:
        logger.error(f"An error occurred while selecting a file or directory: {e}")
