import os
import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def group_files_by_pattern(target_groups: Dict[str, List[str]]) -> Optional[List[Dict[str, List[str]]]]:
    """
    对具有同名但后缀不同或分卷压缩的多个文件路径组成的分组字典进行处理

    :param target_groups: 被处理字典，格式为：{'target_path': '目标路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}
    :return: 包含字典的列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}]
            如果在处理过程中出现异常，则返回 None。
    """
    regexes = {
        'rar_old': re.compile(r"(.*\.r\d\d)"),
        'rar_now': re.compile(r"(.*\.part\d+\.rar)"),
        'rar': re.compile(r"(.*\.rar)"),
        'zip_7z': re.compile(r"(.*\.\d+\.zip)"),
        'zip_winzip': re.compile(r"(.*\.z\d\d)"),
        'zip': re.compile(r"(.*\.zip)"),
        '7z': re.compile(r"(.*\.7z\.\d+)"),
        'split': re.compile(r"(.*\.\d+)")
    }  # 找出常见压缩文件名的正则表达式
    matches = {key: 0 for key in regexes}
    matched_files = {key: [] for key in regexes}
    target_path = target_groups['target_path']
    grouped_file_list = sorted(target_groups['grouped_file_list'])
    other_path_list = []
    full_path_list = []
    part_lists = []

    try:
        for file_name in grouped_file_list:
            for key, regex in regexes.items():
                if regex.match(os.path.basename(file_name)):
                    matches[key] += 1
                    matched_files[key].append(file_name)
                    break

        if matches['rar_old'] > 0 and matches['rar'] == 1:
            main_file = matched_files['rar'][0]
            file_list = matched_files['rar_old'] + matched_files['rar']
            part_lists.append({'target_path': target_path, 'main_file_path': main_file, 'grouped_file_list': file_list})
            other_path_list = list(set(grouped_file_list) - set(file_list))
        elif matches['zip_winzip'] > 0 and matches['zip'] == 1:
            main_file = matched_files['zip'][0]
            file_list = matched_files['zip_winzip'] + matched_files['zip']
            part_lists.append({'target_path': target_path, 'main_file_path': main_file, 'grouped_file_list': file_list})
            other_path_list = list(set(grouped_file_list) - set(file_list))
        elif any(len(matched_files[key]) > 0 for key in regexes):
            for _, v in matched_files.items():
                if len(v) > 0:
                    part_lists.append({'target_path': target_path, 'main_file_path': v[0], 'grouped_file_list': v})
                    full_path_list.extend(v)
            other_path_list = list(set(grouped_file_list) - set(full_path_list))
        else:
            for i in grouped_file_list:
                part_lists.append({'target_path': target_path, 'main_file_path': i, 'grouped_file_list': [i]})

        if len(other_path_list) > 0:
            other_lists = group_files_by_pattern({'target_path': target_path, 'grouped_file_list': other_path_list})
            part_lists.extend(other_lists)

        return part_lists
    except Exception as e:
        logger.error(f"An error occurred while grouping files by pattern: {e}")
        return None
