import os
from typing import List, Dict, Any, Optional
import logging

from modules.file_ops import get_file_type, rename_target_if_exist, get_folder_paths, create_directories, remove_target
from modules.configs.settings import ZIP_FILE_TYPE_DICT

logger = logging.getLogger(__name__)


def group_files_main(full_infos: List[Dict[str, Any]], path_zip: Optional[str] = '', path_dest: Optional[str] = '', force_mode: Optional[int] = 0) -> Optional[List[Dict[str, Any]]]:
    """
    将全文件信息列表（字典）作为输入，筛选出压缩文件信息列表。

    :param full_infos: 要处理的全文件列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
    :type full_infos: List[Dict[str, Any]]
    :param path_zip: 压缩文件路径，缺省时为空字符串。
    :type path_zip: Optional[str]
    :param path_dest: 目标路径，缺省时为空字符串。
    :type path_dest: Optional[str]
    :param force_mode: 是否启用强制模式。
    :type force_mode: Optional[int]
    :rtype: Optional[List[Dict[str, Any]]]
    :return: 返回包含完整字典的列表，格式为：[{'target_path': '目标路径', 'main_file': '主文件路径', 'file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
            如果在处理过程中出现异常，则返回 None。
    """
    file_infos = []
    delete_temp_list = []

    try:
        if path_zip and path_dest:
            path_zip = os.path.normpath(path_zip) + os.sep
            path_dest = os.path.normpath(path_dest) + os.sep
            path_zip_folders = [os.path.normpath(folder) for folder in get_folder_paths(path_zip)]
            temp_folder_list = [folder.replace(path_zip, path_dest) if folder.startswith(path_zip) else folder for folder in path_zip_folders]
            delete_temp_list = create_directories(temp_folder_list) if temp_folder_list else None

        for info in full_infos:
            main_file = info['main_file_path']
            file_list = info['grouped_file_list']
            file_type = 'application/zip' if force_mode else get_file_type(main_file)
            if file_type in ZIP_FILE_TYPE_DICT:
                path = rename_target_if_exist(info['target_path'])
                os.makedirs(path, exist_ok=True)
                file_infos.append({'target_path': path, 'main_file': main_file, 'file_list': file_list})
            else:
                logger.debug(f"{main_file} is not support, the file type is: {file_type}")

        if delete_temp_list:
            list(map(remove_target, delete_temp_list))

        logger.debug(f"file_infos: \n{file_infos}")
        return file_infos
    except Exception as e:
        logger.error(f"An error occurred while grouping files: {e}")
        return None
