import argparse
import locale
import os
import time
from multiprocessing import Pool, freeze_support
from typing import Optional, Union

from modules import *

logger = logging.getLogger(__name__)
logging_config(console_output=True)


# noinspection DuplicatedCode,PyShadowingNames
def main(path_zip: Union[str, os.PathLike], password: Optional[str], parallel: str) -> int:
    """
    Command-line mode\n
    Package：pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin/7z.exe;bin' --add-binary 'bin/7z.dll;bin' --console BrutalityExtractorCli.py
    :type path_zip: Union[str, os.PathLike]
    :param path_zip: Directory containing the compressed files
    :type password: Optional[str]
    :param password: Password for the compressed file
    :type parallel: str
    :param parallel: Number of processes
    :rtype: int
    :return: Return status code
    :raise Exception: If error return 1
    """
    try:
        path_zip = str(path_zip)
        password = str(password) if password else ''
        parallel = int(parallel) if parallel.isdigit() else 1

        print('BrutalityExtractor Copyright 2023 by assassing')
        logger.info(LANG["main_info_start"].format("#" * 6, "#" * 6))

        file_paths = get_file_paths(path_zip)
        if not file_paths:
            logger.warning(LANG["main_no_file_warning"].format("#" * 6, path_zip, "#" * 6))
            return 1

        path_groups = group_file_paths(file_paths)

        full_infos = group_list_by_lens(path_groups)

        file_infos = group_files_main(full_infos)
        if not file_infos:
            logger.warning(LANG["main_no_file_infos_warning"].format("#" * 6, path_zip, "#" * 6))
            return 1

        file_size = sum(get_target_size(p) for i in file_infos for p in i['file_list'])
        file_size_format = format_size(file_size)
        password_list = list(set(read_file_to_list(password) if os.path.isfile(password) else [password]))
        thread_pool = Pool(processes=parallel)
        failed_counts = 0
        start_time = time.time()

        def print_result(result):
            nonlocal failed_counts
            if result['code'] == 0:
                [remove_target(file_del) for file_del in result['file_info']['file_list']]
            else:
                remove_target(result['file_info']['target_path']) if os.path.exists(result['file_info']['target_path']) else None
                failed_counts += 1

        for file_info in file_infos:
            thread_pool.apply_async(file_unzip, args=(file_info, password_list), callback=print_result)

        thread_pool.close()
        thread_pool.join()

        elapsed_time = round(time.time() - start_time, 2)
        your_speed = calculate_transfer_speed(file_size, elapsed_time)
        file_in_total_number = len(file_infos)
        finished_counts = file_in_total_number - failed_counts

        logger.info(LANG["main_info_done"].format('#' * 6, '#' * 6, file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time, your_speed))
        return 0

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1


if __name__ == '__main__':
    LANG = LANG_DICT['CHS'] if locale.getdefaultlocale()[0] == 'zh_CN' else LANG_DICT['ENG']
    freeze_support()
    # main(r'B:\2', 'str ', '16')

    parser = argparse.ArgumentParser(
        description='The password is allowed to be empty, and if the password contains spaces, enclose it with double quotation marks "".',
        epilog='BrutalityExtractor Copyright 2023 by assassing\n'
    )
    parser.add_argument('-d', default=None, required=True, help='directory with zip files')
    parser.add_argument('-p', default='', help='password or text with password (optional)')
    parser.add_argument('-c', default='1', help='set up your speed (optional)')
    parser.add_argument('-v', '--version', action='version', version='BrutalityExtractor v1.1.0')

    args = parser.parse_args()

    main(args.d, args.p, args.c)
