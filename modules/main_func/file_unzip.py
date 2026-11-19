import logging
import os
import re
import shutil
import subprocess
from typing import Any, Dict, List, Set, Union

from modules.file_ops import get_file_paths, get_resource_path
from modules.main_func.group_file_paths import group_file_paths
from modules.main_func.group_files_main import group_files_main
from modules.main_func.group_list_by_lens import group_list_by_lens

logger = logging.getLogger(__name__)
BIN_7Z_PATH = get_resource_path('bin/7z.exe')


def _file_unzip_once(file_info: Dict[str, Any], password_set: Set[str]) -> Dict[str, Union[int, Dict[str, Any]]]:
    """Extract one archive and return the existing result structure."""
    target_path = file_info['target_path']
    main_file = file_info['main_file']
    file_list = file_info['file_list']
    result_data = {'code': -1, 'file_info': file_info}

    if not password_set:
        password_set = {''}

    for passwd in password_set:
        unzip_command = [BIN_7Z_PATH, 'x', '-aoa', f'-o{target_path}', f'-p{passwd}', '--', f'{main_file}']

        try:
            if os.name == 'nt':
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(unzip_command, capture_output=True, startupinfo=si)
            else:
                result = subprocess.run(unzip_command, capture_output=True)
            stdout_text = result.stdout.decode('utf-8', 'ignore').strip()
            stderr_text = result.stderr.decode('utf-8', 'ignore').strip()
            logger.debug(f"Command: {unzip_command}\nOutput:\n{stdout_text}\n{stderr_text}")
        except Exception as e:
            logger.warning(f"Command execution failed: {unzip_command}, Error message: {e}")
            return result_data

        if result.returncode == 0:
            result_data['code'] = 0
            logger.info(f"Decompression Success : {main_file}")
            return result_data
        if result.returncode == 2 and re.search(r"Wrong password", stderr_text):
            result_data['code'] = 2
            logger.debug(f"Decompression Failed : {main_file}, wrong password: {passwd}")
            continue
        if result.returncode == 2 and re.search(r"Cannot open the file as archive", stderr_text):
            result_data['code'] = 3
            logger.warning(f"Decompression Failed : {main_file}, unsupported file type")
            return result_data
        if result.returncode == 2 and re.search(r"系统找不到指定的|Cannot find", stderr_text):
            result_data['code'] = 4
            logger.warning(f"Decompression Failed : {main_file}, compressed file not found")
            return result_data
        if result.returncode == 2 and re.search(r"Missing volume :", stderr_text):
            result_data['code'] = 5
            missing_volume = re.search(r"Missing volume : (.*)", stderr_text)
            logger.warning(f"Decompression Failed : {main_file}, missing volume: {missing_volume.group(1) if missing_volume else None}")
            return result_data
        if result.returncode == 2 and re.search(r"CRC Failed|CRC Error", stderr_text):
            result_data['code'] = 6
            logger.warning(f"Decompression Failed : {main_file}, CRC checksum failed")
            return result_data
        if result.returncode == 2 and re.search(r"Headers Error", stderr_text):
            result_data['code'] = 7
            logger.warning(f"Decompression Failed : {main_file}, file headers error")
            return result_data
        if result.returncode == 2 and re.search(r"Unexpected end of archive", stderr_text):
            result_data['code'] = 8
            logger.warning(f"Decompression Failed : {main_file}, unexpected end of archive")
            return result_data
        if result.returncode == 2 and re.search(r"Data Error :", stderr_text):
            result_data['code'] = 9
            logger.warning(f"Decompression Failed : {main_file}, file is corrupted")
            return result_data
        result_data['code'] = 10
        logger.warning(f"Decompression Failed : {main_file}, error code: {result.returncode}, error info: {result.stderr}")
        return result_data

    result_data['code'] = 2
    logger.warning(f"Decompression Failed : {main_file}, all passwords failed")
    return result_data


def _get_nested_file_infos(
        target_path: str,
        processed_archives: Set[str],
        protected_archives: Set[str] = None
) -> List[Dict[str, Any]]:
    """Find unprocessed supported archives below an extraction target."""
    protected_archives = protected_archives or set()
    file_paths = get_file_paths(target_path)
    if not file_paths:
        return []
    path_groups = group_file_paths(file_paths)
    if not path_groups:
        return []
    full_infos = group_list_by_lens(path_groups)
    if not full_infos:
        return []
    unprocessed_infos = [
        info for info in full_infos
        if os.path.normcase(os.path.abspath(info['main_file_path'])) not in processed_archives
        and os.path.normcase(os.path.abspath(info['main_file_path'])) not in protected_archives
    ]
    return group_files_main(unprocessed_infos) or []


def _extract_nested_archives(
        target_path: str,
        password_set: Set[str],
        remove_source: bool = False,
        protected_archives: Set[str] = None
) -> None:
    """Extract nested archives until the target contains no unprocessed archives."""
    processed_archives: Set[str] = set()
    protected_archives = protected_archives or set()
    while True:
        file_infos = _get_nested_file_infos(target_path, processed_archives, protected_archives)
        if not file_infos:
            return
        for file_info in file_infos:
            archive_key = os.path.normcase(os.path.abspath(file_info['main_file']))
            processed_archives.add(archive_key)
            nested_result = _file_unzip_once(file_info, password_set)
            if nested_result['code'] == 0:
                for source_file in file_info['file_list']:
                    try:
                        if os.path.exists(source_file):
                            os.remove(source_file)
                    except OSError as e:
                        logger.warning(f"Unable to remove nested archive '{source_file}': {e}")
            else:
                logger.warning(f"Nested archive extraction failed: {file_info['main_file']}")


def flatten_extracted_output(target_path: str) -> None:
    """Move extracted files to the target root and remove intermediate directories."""
    target_path = os.path.abspath(target_path)
    if not os.path.isdir(target_path):
        return

    for root, _, file_names in os.walk(target_path, topdown=True):
        root = os.path.abspath(root)
        for file_name in file_names:
            source_path = os.path.join(root, file_name)
            if os.path.normcase(root) == os.path.normcase(target_path):
                continue
            destination_path = os.path.join(target_path, file_name)
            if os.path.exists(destination_path):
                base_name, extension = os.path.splitext(file_name)
                counter = 1
                while True:
                    destination_path = os.path.join(target_path, f"{base_name}_{counter}{extension}")
                    if not os.path.exists(destination_path):
                        break
                    counter += 1
            shutil.move(source_path, destination_path)

    for root, directory_names, _ in os.walk(target_path, topdown=False):
        root = os.path.abspath(root)
        if os.path.normcase(root) == os.path.normcase(target_path):
            continue
        try:
            os.rmdir(root)
        except OSError:
            shutil.rmtree(root)


def file_unzip(
        file_info: Dict[str, Any],
        password_set: Set[str],
        remove_source: bool = False
) -> Dict[str, Union[int, Dict[str, Any]]]:
    """
    Extract an archive and recursively extract supported archives found in its target.

    :param file_info: Archive information with target_path, main_file, and file_list.
    :param password_set: Candidate passwords.
    :param remove_source: Remove nested archives after successful extraction.
    """
    result_data = _file_unzip_once(file_info, password_set)
    if result_data['code'] == 0:
        protected_archives = {
            os.path.normcase(os.path.abspath(source_file))
            for source_file in file_info['file_list']
        }
        _extract_nested_archives(
            file_info['target_path'],
            password_set,
            remove_source,
            protected_archives,
        )
        flatten_extracted_output(file_info['target_path'])
    return result_data
