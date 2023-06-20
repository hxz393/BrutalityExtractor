import logging
import os
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


# noinspection DuplicatedCode
def get_file_paths(target_path: Union[str, os.PathLike]) -> Optional[List[str]]:
    """
    获取目标目录下所有文件的路径。

    :type target_path: Union[str, os.PathLike]
    :param target_path: 目标目录的路径，可以是字符串或 os.PathLike 对象。
    :rtype: Optional[List[str]]
    :return: 一个列表，包含所有文件的路径，或者在发生错误时返回 None。
    """
    try:
        if not os.path.exists(target_path):
            logger.error(f"The path '{target_path}' does not exist.")
            return None
        if not os.path.isdir(target_path):
            logger.error(f"'{target_path}' is not a valid directory.")
            return None
        file_paths = [os.path.normpath(os.path.join(root, file)) for root, _, files in os.walk(target_path) for file in files]
        logger.debug(f"file_paths: \n{file_paths}")
        return file_paths
    except Exception as e:
        logger.error(f"An error occurred while retrieving file paths: {e}")
        return None
