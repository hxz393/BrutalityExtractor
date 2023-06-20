import configparser
import logging
from pathlib import Path

from filelock import FileLock

from modules.configs.lang_dict import LANG_DICT
from modules.configs.settings import *
from modules.module_use import config_read, config_get

logger = logging.getLogger(__name__)

lock = FileLock("config.lock")

with lock:
    CP = configparser.ConfigParser()
    # 如果配置文件存在，读取配置文件
    if Path(CONFIG_PATH).exists():
        CP = config_read(CONFIG_PATH)
    else:
        logger.error(f"Configuration file does not exist: {CONFIG_PATH}")

    # 先更新 "DEFAULT" section，不论是否已经存在
    CP.read_dict(DEFAULT_CONFIG)

    # 检查是否存在 "main" section，如果不存在则添加
    if not CP.has_section("main"):
        CP.add_section("main")

    # 最后写入配置文件
    try:
        with open(CONFIG_PATH, 'w', encoding="utf-8") as configfile:
            CP.write(configfile)
    except Exception as e:
        logger.error(f"An error occurred while writing to the configuration file: {e}")

# 使用包装函数获取配置值
path_zip_config = config_get(CP, 'main', 'path_zip', CP.get)
path_dest_config = config_get(CP, 'main', 'path_dest', CP.get)
password_config = config_get(CP, 'main', 'password', CP.get)
parallel_config = config_get(CP, 'main', 'parallel', CP.getint)
no_warnning_config = config_get(CP, 'main', 'no_warnning', CP.getint)
is_delete_config = config_get(CP, 'main', 'is_delete', CP.getint)
log_level_config = config_get(CP, 'main', 'log_level', CP.get)
log_size_config = config_get(CP, 'main', 'log_size', CP.getint)
log_count_config = config_get(CP, 'main', 'log_count', CP.getint)
is_extra_config = config_get(CP, 'main', 'is_extra', CP.getint)
is_redundant_config = config_get(CP, 'main', 'is_redundant', CP.getint)
is_empty_config = config_get(CP, 'main', 'is_empty', CP.getint)
xcl_dir_config = config_get(CP, 'main', 'xcl_dir', CP.get)
xcl_file_config = config_get(CP, 'main', 'xcl_file', CP.get)
no_tooltip_config = config_get(CP, 'main', 'no_tooltip', CP.getint)
mini_skin_config = config_get(CP, 'main', 'mini_skin', CP.getint)
theme_config = config_get(CP, 'main', 'theme', CP.get)
lang_config = config_get(CP, 'main', 'lang', CP.get)
alpha_config = config_get(CP, 'main', 'alpha', CP.getfloat)

# 校准配置
theme_config = theme_config if theme_config in THEME_LIST else 'yeti'
log_level_config = log_level_config if log_level_config in LOG_LEVEL_LIST else 'INFO'
lang_config = lang_config if lang_config in LANG_LIST else 'ENG'

# 图标
FONT_SIZE = 10 if mini_skin_config else 16
ICO_SIZE = 16 if mini_skin_config else 48

# 初始化语言配置
LANG = LANG_DICT[lang_config]

# 初始化日志字典
LOG_CONFIG_DICT = {
    'console_output': True,
    'log_file': LOG_PATH,
    'log_level': log_level_config,
    'max_log_size': log_size_config,
    'backup_count': log_count_config,
}
