import os
import sys
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)


def get_resource_path(relative_path: Union[str, os.PathLike]) -> Optional[str]:
    """
    获取资源的绝对路径。这个函数适用于 PyInstaller 打包后的可执行文件。\n
    测试打包：pyinstaller -F my_module/file_ops/get_resource_path.py\n
    测试运行：.\dist\get_resource_path.exe\n

    :type relative_path: Union[str, os.PathLike]
    :param relative_path: 相对路径，可以是字符串或 os.PathLike 对象。
    :rtype: Optional[str]
    :return: 资源的绝对路径，如果发生错误则返回 None。
    """

    try:
        if not isinstance(relative_path, (str, os.PathLike)):
            logger.error(f"The input relative path '{relative_path}' should be of type str or os.PathLike.")
            return None

        relative_path = os.path.normpath(relative_path)
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
    except Exception as e:
        logger.error(f"An error occurred while retrieving resource path: {e}")
        return None
