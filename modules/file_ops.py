from pathlib import Path
import json
from logging import getLogger
import configparser
import base64
import uuid
import tempfile
import magic
from collections import defaultdict
import shutil
import re
import os
from typing import Dict, List, Any

ZIP_FILE_TYPE_DICT = {
    'application/x-bzip2': '.bz2',
    'application/x-gzip': '.gz',
    'application/x-rar': '.rar',
    'application/x-tar': '.tar',
    'application/x-xz': '.xz',
    'application/zip': '.zip',
    'application/x-7z-compressed': '.7z'
}


def get_file_paths(target: str, logger) -> list[str]:
    """
    获取目标目录下的所有文件路径列表

    :param target: 检测目录
    :param logger: 日志记录器
    :return: 文件路径列表
    """
    path = Path(target)
    file_paths = []

    try:
        if not path.exists() or not path.is_dir():
            logger.warning(f'源目录 {target} 不存在或不是有效的目录路径')
        else:
            file_paths = [str(file_path) for file_path in path.rglob('*') if file_path.is_file()]
            logger.debug(f'获取目录 {target} 下的文件列表完成，文件列表如下：\n{file_paths}')
    except Exception as e:
        logger.error(f'获取目录 {target} 下的文件列表失败: \n{str(e)}')

    return file_paths


def get_folder_paths(target: str, logger) -> list[str]:
    """
    获取目标目录下的所有文件夹路径列表

    :param target: 检测目录
    :param logger: 日志记录器
    :return: 文件夹路径列表
    """
    path = Path(target)
    folder_paths = []

    try:
        if not path.exists() or not path.is_dir():
            logger.warning(f'源目录 {target} 不存在或不是有效的目录路径')
        else:
            for entry in path.iterdir():
                if entry.is_dir():
                    folder_paths.append(str(entry))
                    folder_paths.extend(get_folder_paths(str(entry),logger))
            logger.debug(f'获取目录 {target} 下的文件夹列表完成，文件列表如下：\n{folder_paths}')
    except Exception as e:
        logger.error(f'获取目录 {target} 下的文件夹列表失败: \n{str(e)}')

    return folder_paths


def get_subdirectories(path: str, logger) -> list[str]:
    """
    获取目标目录下的第一级文件夹路径列表

    :param path: 检测目录
    :param logger: 日志记录器
    :return: 文件夹路径列表
    """
    subdirectories = []
    try:
        for item in Path(path).iterdir():
            if item.is_dir():
                subdirectories.append(str(item))
        logger.debug(f'获取目录 {path} 下的子目录列表完成，文件列表如下：\n{subdirectories}')
    except Exception as e:
        logger.error(f'获取目录 {path} 下的子目录列表失败: \n{str(e)}')

    return subdirectories

def get_file_type(file_path: str, logger) -> str:
    """
    以读取文件头的方式，取得指定文件的真实类型

    :param file_path: 要检测的文件路径
    :param logger: 日志记录器
    :return: 文件类型检测结果
    """
    file_type = ""

    try:
        with open(file_path, 'rb') as f:
            file_type = magic.from_buffer(f.read(4096), mime=True)
            logger.debug(f'文件 {file_path} 类型为：{file_type}')
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f'无法获取 {file_path} 文件类型：\n{str(e)}')

    return file_type


def get_target_size(target: str, logger) -> int:
    """
    获取给定文件或文件夹的大小

    :param target: 文件或文件夹的路径
    :param logger: 日志记录器
    :return: 文件或文件夹的大小（字节数）
    """
    path = Path(str(target))
    total_size = 0

    try:
        if path.is_file():
            total_size = path.stat().st_size
        elif path.is_dir():
            total_size = sum(file.stat().st_size for file in path.rglob('*') if file.is_file())
        logger.debug(f'目标 {target} 大小为：{total_size}')
    except Exception as e:
        logger.error(f'无法获取 {target} 大小：\n{str(e)}')

    return total_size


def read_txt_to_list(path: str, logger = getLogger(__name__)) -> list[str]:
    """
    读取文本文件中的内容，并将其存储成列表

    :param path: 文本文件的路径
    :param logger: 日志记录器
    :return: 返回文本内容列表
    """
    content = []

    try:
        with open(path, 'r') as file:
            content = [line.strip() for line in file]
        logger.debug(f'成功读取文本文件: {path}')
    except FileNotFoundError:
        logger.error(f'找不到文本文件: {path}')
    except Exception as e:
        logger.error(f'读取文本文件 {path} 时发生错误: \n{str(e)}')

    return content


def write_str_to_txt(path: str, content: str, logger):
    """
    将字符串写入到文件中

    :param path: 文本文件的路径
    :param content: 要写入的内容
    :param logger: 日志记录器
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file_write:
            file_write.write(content)
        logger.debug(f'成功写入文本文件: {path}')
    except Exception as e:
        logger.error(f'写入文本文件 {path} 时发生错误: \n{str(e)}')


def read_config(path: str, logger = getLogger(__name__)):
    """
    读取配置文件

    :param path: 文本文件的路径
    :param logger: 日志记录器
    :return: 返回配置
    """
    config_parser = configparser.ConfigParser()

    try:
        with open(path, 'r') as f:
            config_parser.read_file(f)
        logger.debug(f'成功读取配置文件: {path}')
    except FileNotFoundError:
        logger.error(f'找不到配置文件: {path}')
        return {}
    except Exception as e:
        logger.error(f'读取配置文件 {path} 时发生错误: \n{str(e)}')
        return {}

    return config_parser


def write_config(path: str, config: dict[str], logger = getLogger(__name__)):
    """
    将配置字典写入到配置文件中

    :param path: 配置文件的路径
    :param config: 要写入的配置字典
    :param logger: 日志记录器
    """
    config_parser = configparser.ConfigParser()

    for section, section_config in config.items():
        config_parser[section] = section_config
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            config_parser.write(f)
        logger.debug(f'成功写入配置文件: {path}')
    except Exception as e:
        logger.error(f'写入配置文件 {path} 时发生错误: \n{str(e)}')


def read_json(path: str, logger = getLogger(__name__)):
    """
    读取 Json 文件

    :param path: Json 文件的路径
    :param logger: 日志记录器
    :return: 返回内容字典
    """
    # # 写入 JSON 数据
    # with open('aa.json', 'w', encoding='utf-8') as f:
    #     json.dump(lang_dict, f, ensure_ascii=False, indent=4)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lang_dict = json.load(f)
        logger.debug(f'成功读取 Json 文件: {path}')
    except FileNotFoundError:
        logger.error(f'找不到 Json 文件: {path}')
        lang_dict = {}
    except Exception as e:
        logger.error(f'读取 Json 文件 {path} 时发生错误: \n{str(e)}')
        lang_dict = {}

    return lang_dict


def get_config(config_parser, section: str, key: str, default_value: str) -> int | str | float:
    """
    获取配置

    :param config_parser:
    :param section: 段落
    :param key: 配置关键字
    :param default_value: 默认值
    """

    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    try:
        if default_value.isdigit():
            return int(config_parser[section][key]) if config_parser[section][key].isdigit() else int(default_value)
        elif is_float(default_value):
            return float(config_parser[section][key]) if is_float(config_parser[section][key]) else float(default_value)
        else:
            return config_parser[section][key]
    except KeyError:
        if default_value.isdigit():
            return int(default_value)
        elif is_float(default_value):
            return float(default_value)
        else:
            return default_value


def create_temp_icon_file(base64_string: str, logger) -> str:
    """
    解码字符串并创建一个临时文件

    :param base64_string: 编码字符
    :param logger: 日志记录器
    :return: 临时文件路径
    """
    path = ''

    try:
        icon_data = base64.b64decode(base64_string)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ico')
        with open(temp_file.name, 'wb') as icon_file:
            icon_file.write(icon_data)
        path = temp_file.name
        logger.debug(f'临时图标文件创建成功：{temp_file.name}')
    except Exception as e:
        logger.error(f'临时图标文件创建失败: \n{str(e)}')

    return path


def remove_target(target: str, logger):
    """
    删除目标路径对应的文件或目录

    :param target: 要删除的文件或目录的路径
    :param logger: 日志记录器
    """
    path = Path(str(target))

    if not path.exists():
        logger.warning(f"要删除目标 {target} 不存在")
        return

    try:
        if path.is_dir():
            shutil.rmtree(path, onerror=remove_permissions)
        elif path.is_file():
            path.unlink()
        else:
            logger.warning(f"删除目标 {target} 失败，目标可能是一个特殊文件类型")
            return
    except PermissionError:
        logger.warning(f"删除目标 {target} 失败，去除权限后重试")
        remove_permissions(lambda x: None, path, None)
        path.unlink()
    except Exception as e:
        logger.error(f"删除目标 {target} 失败: \n{e}")


def remove_permissions(func, path: Path, _):
    """
    去除目标路径的权限并调用指定的函数

    :param func: 要调用的函数
    :param path: 目标路径
    :param _ : 用于异常处理的错误信息
    """
    path.chmod(0o777)
    func(path)



def remove_matched(paths: list[str], logger, pattern_set: set[str]):
    """
    删除匹配排除列表集合的目标

    :param paths: 路径列表
    :param logger: 日志记录器
    :param pattern_set: 排除列表集合
    """
    try:
        matched_paths = [path for path, basename in zip(paths, [os.path.basename(path) for path in paths]) if basename in pattern_set]

        for path in matched_paths:
            remove_target(path, logger)
            logger.info(f"目标 {path} 匹配排除列表，已被删除")
    except Exception as e:
        logger.error(f"匹配排除列表时发生错误: \n{e}")


def remove_redundant(path: str, logger):
    """
    消除冗余目录结构

    :param path: 目标路径
    :param logger: 日志记录器
    """
    path = Path(path)
    try:
        subdirs = [subdir for subdir in path.iterdir() if subdir.is_dir()]

        if len(subdirs) == 1 and subdirs[0].name == path.name:
            subdir_path = subdirs[0]
            parent_files = [file for file in path.iterdir() if file.is_file()]

            if not parent_files:
                temp_dir = path / f"{subdir_path.name}_{uuid.uuid4()}"
                subdir_path.rename(temp_dir)

                for item in temp_dir.iterdir():
                    item.rename(path / item.name)

                if not list(temp_dir.iterdir()):
                    temp_dir.rmdir()
                    logger.info(f"目标 {path} 提取冗余目录完成")
    except Exception as e:
        logger.error(f"提取冗余目录时发生错误: \n{e}")


def remove_empty_dirs(path: str, logger):
    """
    删除所有空目录

    :param path: 目标路径
    :param logger: 日志记录器
    """
    try:
        for p in Path(path).rglob('*'):
            if p.is_dir() and not any(p.iterdir()):
                p.rmdir()
                logger.info(f"空目录 {p} 被删除")
    except Exception as e:
        logger.error(f"删除空目录时发生错误: \n{e}")





def rename_path(path: str, logger, path_set: set[str] = ()) -> tuple[str, set[str]]:
    """
    检测目标路径是否存在于本地或集合中，存在则重命名

    :param path: 被检测的路径
    :param logger: 日志记录器
    :param path_set: 对比路径集合
    :return: 被检测过的路径, 更新过后的对比路径集合
    """
    original_path = path
    suffix = 0

    try:
        while os.path.exists(path) or path.lower() in path_set:
            suffix += 1
            path = f'{original_path}({suffix})'
        path_set.add(path.lower())
    except Exception as e:
        logger.error(f"目标 {path} 重命名失败: \n{e}")

    return path, path_set


def group_file_paths(paths_list: List[str], logger) -> defaultdict[str, list]:
    """
    对文件路径列表进行初步分组，找出可能是分卷压缩或有相同输出路径的文件，生成字典

    :param paths_list: 要处理的文件路径列表
    :param logger: 日志记录器
    :return: 返回字典，格式为：{目标路径1:[文件路径1,文件路径2...],目标路径2:[文件路径1]...}
    """
    archive_regex = re.compile(r"^(.*?)(?:\.part\d+\.rar|\.7z\.\d+|\.r\d\d|\.z\d\d|\.\d+\.zip|\.\d+)$")  # 找出常见分卷压缩文件名的正则表达式
    path_groups = defaultdict(list)

    try:
        for file_path in paths_list:
            match = archive_regex.match(file_path)
            base_path = match.group(1) if match else os.path.splitext(file_path)[0]
            path_groups[base_path].append(file_path)
        logger.debug(f'文件路径列表初步分组完成：\n{path_groups}')
    except Exception as e:
        logger.error(f'文件分组发生错误: \n{str(e)}')

    return path_groups


def group_files_by_pattern(target_groups: dict[str, list], logger) -> list[dict]:
    """
    对具有同名但后缀不同或分卷压缩的多个文件路径组成的分组字典进行处理

    :param target_groups: 被处理字典，格式为：{'target_path': '目标路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}
    :param logger: 日志记录器
    :return: 包含字典的列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}]
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
            other_lists = group_files_by_pattern({'target_path': target_path, 'grouped_file_list': other_path_list}, logger)
            part_lists.extend(other_lists)
        logger.debug(f'多同名文件分组完成：\n{part_lists}')
    except Exception as e:
        logger.error(f'文件分组发生错误: \n{str(e)}')

    return part_lists


def group_list_by_lens(path_groups: dict[str, list], logger) -> list[dict[str, Any]]:
    """
    检测分组文件列表个数，单个的直接加入列表，多个的处理后加入列表

    :param path_groups: 被检测的字典，格式为：{目标路径1:[文件路径1,文件路径2...],目标路径2:[文件路径1]...}
    :param logger: 日志记录器
    :return: 返回带字典的列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
    """
    full_infos = []
    try:
        for path, path_list in path_groups.items():
            if len(path_list) == 1:
                full_infos.append({'target_path': path, 'main_file_path': path_list[0], 'grouped_file_list': path_list})
            else:
                full_infos.extend(group_files_by_pattern({'target_path': path, 'grouped_file_list': path_list}, logger))
        logger.debug(f'按文件列表长度整理成字典完成：\n{full_infos}')
    except Exception as e:
        logger.error(f'按文件列表长度整理发生错误: \n{str(e)}')

    return full_infos


def group_files_main(full_infos: List[Dict[str, Any]], logger) -> List[Dict[str, Any]]:
    """
    接受全文件信息字典列表，筛选出压缩文件文件信息字典列表

    :param full_infos: 要处理的全文件列表，格式为：[{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
    :param logger: 日志记录器
    :return: 返回包含完整字典的列表，格式为：[{'target_path': '目标路径', 'main_file': '主文件路径', 'file_list': ['文件路径1', '文件路径2', '文件路径3'...]}...]
    """
    path_set = set()
    file_infos = []

    try:
        for info in full_infos:
            main_file = info['main_file_path']
            file_list = info['grouped_file_list']
            file_type = get_file_type(main_file, logger)
            if file_type in ZIP_FILE_TYPE_DICT:
                path, path_set = rename_path(info['target_path'], logger, path_set)
                file_infos.append({'target_path': path, 'main_file': main_file, 'file_list': file_list})
            else:
                logger.warning(f'文件 {main_file} 不支持，类型为：{file_type}')
        logger.debug(f'整理压缩文件列表完成，最终文件列表：\n{file_infos}')
    except Exception as e:
        logger.error(f'整理压缩文件列表时发生错误: \n{str(e)}')

    return file_infos


