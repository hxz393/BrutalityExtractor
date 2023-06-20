import logging
import os
import re
from collections import defaultdict
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def group_file_paths(paths_list: List[str]) -> Optional[Dict[str, List[str]]]:
    """
    对文件路径列表进行初步分组，找出可能是分卷压缩或有相同输出路径的文件，生成字典。

    :type paths_list: List[str]
    :param paths_list: 要处理的文件路径列表。
    :rtype: Optional[Dict[str, List[str]]]
    :return: 返回字典，格式为：{目标路径1:[文件路径1,文件路径2...],目标路径2:[文件路径1]...}。
           如果在处理过程中出现异常，则返回 None。
    """
    archive_regex = re.compile(r"^(.*?)(?:\.part\d+\.rar|\.7z\.\d+|\.r\d\d|\.z\d\d|\.\d+\.zip|\.\d+)$")  # 找出常见分卷压缩文件名的正则表达式
    path_groups = defaultdict(list)

    try:
        for file_path in paths_list:
            match = archive_regex.match(file_path)
            base_path = match.group(1) if match else os.path.splitext(file_path)[0]
            path_groups[base_path].append(file_path)
        path_groups = dict(path_groups)
        logger.debug(f"path_groups: \n{path_groups}")
        return path_groups
    except Exception as e:
        logger.error(f"An error occurred while grouping file paths: {e}")
        return None
