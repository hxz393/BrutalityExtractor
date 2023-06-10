import time
import os.path
import locale
import argparse
from multiprocessing import Pool, freeze_support

from modules.log_conf import configure_logging
from modules.file_unzip import unzip
from modules.file_ops import *
from modules.math_until import *
from config.lang import LANG_DICT

logger=configure_logging(log_file=False, console_output=True)

def main(path_zip: str, password: str, parallel: str):
    """
    Command-line mode
    Package：pyinstaller -F -w -i BrutalityExtractor.ico --add-binary 'bin\7z.exe;bin' --add-binary 'bin\7z.dll;bin' --console BrutalityExtractorCli.py

    :param path_zip: Directory containing the compressed files
    :param password: Password for the compressed file
    :param parallel: Number of processes
    :return: Return status code
    """
    path_zip = str(path_zip)
    password = str(password) if password else ''
    parallel = int(parallel) if parallel.isdigit() else 1
    system_language, _ = locale.getdefaultlocale()
    language = 'CHS' if system_language == 'zh_CN' else 'ENG'
    LANG = LANG_DICT[language]


    print('BrutalityExtractor Copyright 2023 by assassing')
    logger.info(LANG["main_info_start"].format("#" * 6, "#" * 6))
    start_time = time.time()

    file_paths = get_file_paths(path_zip, logger)
    if not file_paths:
        logger.warning(LANG["main_no_file_warning"].format("#" * 6, path_zip, "#" * 6))
        return 1

    path_groups = group_file_paths(file_paths, logger)

    full_infos = group_list_by_lens(path_groups, logger)

    file_infos = group_files_main(full_infos, logger)
    if not file_infos:
        logger.warning(LANG["main_no_file_infos_warning"].format("#" * 6, path_zip, "#" * 6))
        return 1

    file_size = sum(get_target_size(p, logger) for i in file_infos for p in i['file_list'])
    file_size_format = format_size(file_size)
    password_list = list(set(read_txt_to_list(password, logger) if os.path.isfile(password) else [password]))
    thread_pool = Pool(processes=parallel)

    def print_result(result):
        return_code = result['code']
        if return_code == 2:
            remove_target(result['file_info']['target_path'], logger) if os.path.exists(result['file_info']['target_path']) else None
        elif return_code == 0:
            [remove_target(file_del, logger) for file_del in result['file_info']['file_list']]

    for file_info in file_infos:
        thread_pool.apply_async(unzip, args=(file_info, password_list, logger), callback=print_result)

    thread_pool.close()
    thread_pool.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_format = format_time(elapsed_time)
    your_speed = calculate_speed(file_size, elapsed_time)
    file_in_total_number = sum(len(i['file_list']) for i in file_infos)
    failed_counts = sum(1 for i in file_infos for p in i['file_list'] if os.path.exists(p))
    finished_counts = file_in_total_number - failed_counts

    logger.info(LANG["main_info_done"].format('#' * 6, '#' * 6, file_in_total_number, failed_counts, finished_counts, file_size_format, parallel, elapsed_time_format, your_speed))
    return 0


if __name__ == '__main__':
    freeze_support()
    # main(r'B:\2', 'str ', '1')

    parser = argparse.ArgumentParser(
        description='The password is allowed to be empty, and if the password contains spaces, enclose it with double quotation marks "".' ,
        epilog='BrutalityExtractor Copyright 2023 by assassing\n'
    )
    parser.add_argument('-d', default=None, required=True, help='directory with zip files')
    parser.add_argument('-p', default='', help='password or text with password (optional)')
    parser.add_argument('-c', default='1', help='set up your speed (optional)')
    parser.add_argument('-v', '--version', action='version', version='BrutalityExtractor v1.0.0')

    args = parser.parse_args()

    main(args.d, args.p, args.c)

