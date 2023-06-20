import logging
import os
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


def read_file_to_list(target_path: Union[str, os.PathLike]) -> Optional[List[str]]:
    """
    读取文本文件中的内容，并将其存储成列表。

    :param target_path: 文本文件的路径，可以是字符串或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :return: 成功时返回文本内容列表，如果遇到错误则返回None。
    :rtype: Optional[List[str]]
    """
    if not os.path.exists(target_path):
        logger.error(f"The file '{target_path}' does not exist.")
        return None
    if not os.path.isfile(target_path):
        logger.error(f"'{target_path}' is not a valid file.")
        return None

    try:
        with open(target_path, 'r', encoding="utf-8") as file:
            return [line.strip() for line in file]
    except PermissionError:
        logger.error(f"Cannot access file '{target_path}', permission denied.")
        return None
    except UnicodeDecodeError:
        logger.error(f"Cannot decode file '{target_path}', please check whether it is in 'UTF-8' format.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while reading the file '{target_path}': {e}")
        return None
