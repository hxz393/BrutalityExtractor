import os
from typing import List, Dict, Any, Optional
import logging

from modules import get_file_type, rename_target_if_exist
from others.settings import ZIP_FILE_TYPE_DICT

logger = logging.getLogger(__name__)


def group_files_main(full_infos: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    """
    接受全文件信息字典列表，筛选出压缩文件信息字典列表。

    :param full_infos: 要处理的全文件列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
    :return: 返回包含完整字典的列表，格式为：[{'target_path': '目标路径', 'main_file': '主文件路径', 'file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
            如果在处理过程中出现异常，则返回 None。
    """
    file_infos = []
    try:
        for info in full_infos:
            main_file = info['main_file_path']
            file_list = info['grouped_file_list']
            file_type = get_file_type(main_file)
            if file_type in ZIP_FILE_TYPE_DICT:
                path = rename_target_if_exist(info['target_path'])
                os.makedirs(path, exist_ok=True)
                file_infos.append({'target_path': path, 'main_file': main_file, 'file_list': file_list})
        return file_infos
    except Exception as e:
        logger.error(f"An error occurred while grouping files: {e}")
        return None
