import logging
import traceback
import os
from typing import List, Union, Optional

from modules.file_ops import remove_target

logger = logging.getLogger(__name__)


def remove_target_matched(target_path: Union[str, os.PathLike], match_list: List[str]) -> Optional[List[str]]:
    """
    删除目标路径下与给定匹配列表中任一名字完全匹配的文件或文件夹。

    :param target_path: 指定的目标路径，可是是字符串或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :param match_list: 需要匹配的目标列表，列表中的每个元素是一个字符串。
    :type match_list: List[str]
    :return: 一个包含被删除路径的列表，如果遇到错误则返回 None。
    :rtype: Optional[List[str]]
    """
    if not os.path.exists(target_path):
        logger.error(f"The path '{target_path}' does not exist.")
        return None

    if not match_list:
        logger.error(f"Match list is empty.")
        return None

    try:
        match_list_lower = [item.lower() if isinstance(item, str) else item for item in match_list]
        matched_paths = [
            os.path.normpath(os.path.join(root, file))
            for root, dirs, files in os.walk(target_path)
            for file in files + dirs
            if file.lower() in match_list_lower
        ]
        for path in matched_paths:
            remove_target(path)
        return matched_paths
    except Exception as e:
        logger.error(f"An error occurred while removing matched targets. Error message: {e}\n{traceback.format_exc()}")
        return None
