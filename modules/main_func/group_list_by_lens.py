from typing import Dict, List, Any, Optional
import logging

from .group_files_by_pattern import group_files_by_pattern

logger = logging.getLogger(__name__)


def group_list_by_lens(path_groups: Dict[str, List[str]]) -> Optional[List[Dict[str, Any]]]:
    """
    检测分组文件列表个数，单个的直接加入列表，多个的处理后加入列表

    :param path_groups: 被检测的字典，格式为：{目标路径1:[文件路径1,文件路径2...],目标路径2:[文件路径1]...}
    :return: 返回带字典的列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
            如果在处理过程中出现异常，则返回 None。
    """
    full_infos = []
    try:
        for path, path_list in path_groups.items():
            if len(path_list) == 1:
                full_infos.append({'target_path': path, 'main_file_path': path_list[0], 'grouped_file_list': path_list})
            else:
                full_infos.extend(group_files_by_pattern({'target_path': path, 'grouped_file_list': path_list}))
        logger.debug(f"full_infos: \n{full_infos}")
        return full_infos
    except Exception as e:
        logger.error(f"An error occurred while grouping list by lengths: {e}")
        return None
