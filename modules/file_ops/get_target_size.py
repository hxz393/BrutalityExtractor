import logging
import traceback
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Union, Optional

logger = logging.getLogger(__name__)


def get_file_size(file_path: Union[str, os.PathLike]) -> Optional[int]:
    """
    获取单个文件的大小。

    :param file_path: 单个文件的路径，可以是 str 或 os.PathLike 对象。
    :type file_path: Union[str, os.PathLike]
    :return: 文件的大小（字节数）或者在有错误时返回None。
    :rtype: Optional[int]
    """
    if not os.path.exists(file_path):
        logger.error(f"The file '{file_path}' does not exist.")
        return None
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"An error occurred while getting file size: {e}\n{traceback.format_exc()}")
        return None


def get_target_size(target_path: Union[str, os.PathLike]) -> Optional[int]:
    """
    获取目标文件或文件夹的大小。

    :param target_path: 文件或文件夹的路径，可以是 str 或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :return: 文件或文件夹的大小（字节数）或者在有错误时返回None。
    :rtype: Optional[int]
    """
    if not os.path.exists(target_path):
        logger.error(f"The path '{target_path}' does not exist.")
        return None
    try:
        if os.path.isfile(target_path):
            return get_file_size(target_path)
        elif os.path.isdir(target_path):
            with ThreadPoolExecutor() as executor:
                sizes = executor.map(get_file_size, (os.path.join(dirpath, f) for dirpath, dirnames, filenames in os.walk(target_path) for f in filenames))
            return sum(sizes) if sizes else None
        else:
            logger.error(f"'{target_path}' is not a file or a directory.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while getting target size: {e}\n{traceback.format_exc()}")
        return None
