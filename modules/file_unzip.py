import re
import subprocess
import sys
import os
from pathlib import Path

from modules.file_ops import get_target_size


def get_resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

BIN_7Z_PATH = get_resource_path('bin/7z.exe')


def unzip(file_info: dict, password_set: set, logger) -> dict[str, str | int]:
    """
    解压文件函数

    :param file_info: 文件信息字典，格式为：{'target_path': '目标路径', 'main_file_path': '主文件路径', 'grouped_file_list': ['文件路径1', '文件路径2', '文件路径3'...]}
    :param password_set: 密码集合，格式为：{'pass1', 'pass2'...}
    :param logger: 日志记录器

    :return: 返回解压结果字典，格式为：{'code': 2, 'std': f"", 'file_info': file_info}
    """
    target_path = file_info['target_path']
    main_file = file_info['main_file']
    result_data = {'code': 2, 'std': f"", 'file_info': file_info}

    if not password_set:
        password_set = {''}

    for passwd in password_set:
        unzip_command = [BIN_7Z_PATH, 'x', '-aoa', f'-o{target_path}', f'-p{passwd}', f'--', f'{main_file}']

        try:
            if os.name == 'nt':  # check if the OS is Windows
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                result = subprocess.run(unzip_command, capture_output=True, text=True, startupinfo=si)
            else:
                result = subprocess.run(unzip_command, capture_output=True, text=True)
        except Exception as e:
            result_data['code'] = 1
            result_data['std'] = f"命令执行失败：{unzip_command}，错误信息：{str(e)}"
            logger.warning(result_data['std'])
            return result_data
        logger.debug(f'解压命令：{unzip_command}\n命令输出：\n{result.stdout.strip()}')

        if result.returncode == 0:
            info_size = int(re.search(r"Size:\s+(\d+)", result.stdout).group(1)) if re.search(r"Size:\s+(\d+)", result.stdout) else 0
            size_target = sum(get_target_size(str(f), logger) for f in Path(target_path).rglob('*') if f.is_file())
            if info_size == size_target:
                result_data['code'] = 0
                result_data['std'] = f'文件解压成功：{main_file}'
                logger.info(result_data['std'])
                return result_data
            else:
                result_data['std'] = f'文件解压失败：{main_file}，目标大小不匹配'
                logger.warning(result_data['std'])
                return result_data
        elif result.returncode == 2 and re.search(r"Wrong password", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，错误密码：{passwd}'
            logger.debug(result_data['std'])
            continue
        elif result.returncode == 2 and re.search(r"Cannot open the file as archive", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，不支持的文件类型'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"系统找不到指定的", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，找不到压缩文件'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"Missing volume :", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，缺少分卷：{re.search(r"Missing volume : (.*)", result.stderr).group(1) if re.search(r"Missing volume : (.*)", result.stderr) else None}'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"CRC Failed|CRC Error", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，CRC校验失败'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"Headers Error", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，文件头错误'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"Unexpected end of archive", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，文件不完整'
            logger.warning(result_data['std'])
            return result_data
        elif result.returncode == 2 and re.search(r"Data Error :", result.stderr):
            result_data['std'] = f'文件解压失败：{main_file}，文件已损坏'
            logger.warning(result_data['std'])
            return result_data
        else:
            result_data['std'] = f'文件解压失败：{main_file}，错误代码：{result.returncode}'
            logger.warning(result_data['std'])
            logger.error(result.stderr)
            return result_data
    result_data['std'] = f'文件解压失败：{main_file}，匹配密码全部失败'
    logger.warning(result_data['std'])
    return result_data
