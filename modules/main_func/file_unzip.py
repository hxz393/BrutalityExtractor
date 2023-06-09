import logging
import os
import re
import subprocess
from typing import Set, Dict, Union

from modules.file_ops import get_target_size, get_resource_path

logger = logging.getLogger(__name__)
BIN_7Z_PATH = get_resource_path('bin/7z.exe')


def file_unzip(file_info: Dict[str, Union[str, list]], password_set: Set[str]) -> Dict[str, Union[int, Dict[str, Union[str, list]]]]:
    """
    解压文件函数

    :param file_info: 文件信息字典，格式为：{'target_path': '目标路径', 'main_file': '主文件路径', 'file_list': ['文件路径1', '文件路径2', '文件路径3'...]}
    :type file_info: Dict[str, Union[str, list]]
    :param password_set: 密码集合，格式为：{'pass1', 'pass2'...}
    :type password_set: Set[str]

    :return: 返回解压结果字典，格式为：{'code': 状态码, 'file_info': 原始file_info字典}
    :rtype: Dict[str, Union[int, Dict[str, Union[str, list]]]]
    """
    target_path = file_info['target_path']
    main_file = file_info['main_file']
    result_data = {'code': -1, 'file_info': file_info}

    if not password_set:
        password_set = {''}

    for passwd in password_set:
        unzip_command = [BIN_7Z_PATH, 'x', '-aoa', f'-o{target_path}', f'-p{passwd}', f'--', f'{main_file}']

        try:
            if os.name == 'nt':
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(unzip_command, capture_output=True, text=True, startupinfo=si)
            else:
                result = subprocess.run(unzip_command, capture_output=True, text=True)
        except Exception as e:
            result_data['code'] = -1
            logger.warning(f"Command execution failed: {unzip_command}, Error message: {e}")
            return result_data

        logger.debug(f"Command: {unzip_command}\nOutput:\n{result.stdout.strip()}\n{result.stderr.strip()}")

        if result.returncode == 0:
            info_size = int(re.search(r"Size:\s+(\d+)", result.stdout).group(1)) if re.search(r"Size:\s+(\d+)", result.stdout) else 0
            if info_size == get_target_size(target_path):
                result_data['code'] = 0
                logger.info(f"Decompression Success : {main_file}")
                return result_data
            else:
                result_data['code'] = 1
                logger.warning(f"Decompression Failed : {main_file}, target size mismatch")
                return result_data
        elif result.returncode == 2 and re.search(r"Cannot open encrypted archive. Wrong password", result.stderr):
            result_data['code'] = 2
            logger.debug(f"Decompression Failed : {main_file}, wrong password: {passwd}")
            continue
        elif result.returncode == 2 and re.search(r"Cannot open the file as archive", result.stderr):
            result_data['code'] = 3
            logger.warning(f"Decompression Failed : {main_file}, unsupported file type")
            return result_data
        elif result.returncode == 2 and re.search(r"系统找不到指定的|Cannot find", result.stderr):
            result_data['code'] = 4
            logger.warning(f"Decompression Failed : {main_file}, compressed file not found")
            return result_data
        elif result.returncode == 2 and re.search(r"Missing volume :", result.stderr):
            result_data['code'] = 5
            logger.warning(
                f'Decompression Failed : {main_file}, missing volume: {re.search(r"Missing volume : (.*)", result.stderr).group(1) if re.search(r"Missing volume : (.*)", result.stderr) else None}')
            return result_data
        elif result.returncode == 2 and re.search(r"CRC Failed|CRC Error", result.stderr):
            result_data['code'] = 6
            logger.warning(f"Decompression Failed : {main_file}, CRC checksum failed")
            return result_data
        elif result.returncode == 2 and re.search(r"Headers Error", result.stderr):
            result_data['code'] = 7
            logger.warning(f"Decompression Failed : {main_file}, file headers error")
            return result_data
        elif result.returncode == 2 and re.search(r"Unexpected end of archive", result.stderr):
            result_data['code'] = 8
            logger.warning(f"Decompression Failed : {main_file}, unexpected end of archive")
            return result_data
        elif result.returncode == 2 and re.search(r"Data Error :", result.stderr):
            result_data['code'] = 9
            logger.warning(f"Decompression Failed : {main_file}, file is corrupted")
            return result_data
        else:
            result_data['code'] = 10
            logger.warning(f"Decompression Failed : {main_file}, error code: {result.returncode}, error info: {result.stderr}")
            return result_data
    result_data['code'] = 2
    logger.warning(f"Decompression Failed : {main_file}, all passwords failed")
    return result_data
