import logging
import os
from typing import List, Optional, Union

logger = logging.getLogger(__name__)


def get_folder_paths(target_path: Union[str, os.PathLike]) -> Optional[List[str]]:
    """
    获取目标目录下扫描到的所有文件夹路径

    :type target_path: Union[str, os.PathLike]
    :param target_path: 目标目录的路径，可以是字符串或 os.PathLike 对象。
    :rtype: Optional[List[str]]
    :return: 文件夹路径列表，如果出现错误，则返回 None。
    """

    try:
        target_path = os.path.normpath(target_path)
        if not os.path.exists(target_path):
            logger.error(f"The path '{target_path}' does not exist.")
            return None
        if not os.path.isdir(target_path):
            logger.error(f"'{target_path}' is not a valid directory.")
            return None

        return [os.path.normpath(os.path.join(root, dir_name)) for root, dirs, _ in os.walk(target_path) for dir_name in dirs]
    except Exception as e:
        logger.error(f"An error occurred while retrieving folder paths: {e}")
        return None
