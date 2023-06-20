import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


def create_directories(path_list: List[str]) -> Optional[List[str]]:
    """
    创建不存在的目录。

    :param path_list: 目录路径列表。
    :type path_list: List[str]
    :return: 成功创建的目录列表，如果输入列表为空，则返回None。
    :rtype: Optional[List[str]]
    """
    if not path_list:
        logger.error("The directory list is empty.")
        return None

    success_list = []
    for path in path_list:
        path = os.path.normpath(path)

        filename = os.path.split(path)[-1]
        if len(path) > 260 or any(char in filename for char in r'<>:"/\|?*'):
            logger.error(f"The directory path {path} is invalid.")
            continue

        if not os.path.exists(path):
            try:
                os.makedirs(path)
                success_list.append(path)
            except OSError:
                logger.error(f"Failed to create the directory {path}.")
                continue

    return success_list
