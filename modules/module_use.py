import configparser
import logging
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from typing import Optional, Dict, Any, Union



# noinspection PyShadowingNames
def logging_config(log_file: Optional[str] = None,
                   console_output: bool = False,
                   log_level: str = 'INFO',
                   max_log_size: int = 10,
                   backup_count: int = 10,
                   default_log_format: str = '%(asctime)s - %(levelname)s - %(module)s::%(funcName)s::%(lineno)d - %(message)s'
                   ) -> logging.Logger:
    """
    配置日志记录器，可选在控制台输出，也可选择记录到日志文件。

    :param log_file: 日志文件路径，如果不为空则保存日志到文件
    :type log_file: Optional[str]
    :param console_output: 是否在控制台上输出日志
    :type console_output: bool
    :param log_level: 日志等级，默认为'INFO'
    :type log_level: str
    :param max_log_size: 最大日志文件大小（MB），默认为10MB
    :type max_log_size: int
    :param backup_count: 保留的备份日志文件数量，默认为10
    :type backup_count: int
    :param default_log_format: 日志的默认格式
    :type default_log_format: str
    :rtype: logging.Logger
    :raise ValueError: 如果日志等级不在允许的列表中，将抛出此异常
    :return: 配置后的日志记录器实例
    """
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    if log_level.upper() not in log_levels:
        raise ValueError(f"Invalid log level: {log_level}, it must be one of {log_levels}")

    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    formatter = Formatter(default_log_format)

    if console_output:
        ch = StreamHandler()
        ch.setLevel(getattr(logging, log_level.upper()))
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
        fh = RotatingFileHandler(log_file, maxBytes=max_log_size * 1024 * 1024, backupCount=backup_count, encoding="utf-8")
        fh.close()
        fh.setLevel(getattr(logging, log_level.upper()))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger



# noinspection PyShadowingNames
def config_read(target_path: Union[str, Path]) -> Optional[configparser.ConfigParser]:
    """
    从指定的路径读取配置文件。

    :param target_path: 配置文件的路径。
    :type target_path: Union[str, Path]
    :rtype: Optional[configparser.ConfigParser]
    :raise FileNotFoundError: 如果路径不存在，抛出 FileNotFoundError。
    :raise NotADirectoryError: 如果路径是一个目录，抛出 NotADirectoryError。
    :raise Exception: 如果在处理过程中出现其它问题，抛出一般性的 Exception。
    :return: 如果文件读取成功，返回一个 configparser.ConfigParser 对象；如果文件读取失败，返回 None。
    """
    target_path = Path(target_path)

    if not target_path.exists():
        raise FileNotFoundError(f"The path '{target_path}' does not exist.")
    if target_path.is_dir():
        raise NotADirectoryError(f"The path '{target_path}' is a directory.")

    config_parser = configparser.ConfigParser()
    try:
        with open(target_path, 'r') as f:
            config_parser.read_file(f)
    except Exception as e:
        raise Exception(f"An error occurred while reading the config file {target_path}: {e}")

    return config_parser



def config_write(target_path: Union[str, Path], config: Dict[str, Union[str, Any]]) -> None:
    """
    将配置字典写入配置文件。

    :param target_path: 配置文件的路径。
    :type target_path: Union[str, Path]
    :param config: 配置字典，其中键为节名，值为包含该节配置项的字典。
    :type config: Dict[str, Any]
    :raises ValueError: 当路径或配置为空时引发。
    :raises Exception: 当尝试写入文件失败时引发。
    """
    if not target_path:
        raise ValueError("Path should not be empty.")
    if not config:
        raise ValueError("Config should not be empty.")

    config_parser = configparser.ConfigParser()

    for section, section_config in config.items():
        config_parser[section] = {k: str(v) for k, v in section_config.items()}

    try:
        path = Path(target_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            config_parser.write(f)
    except Exception as e:
        raise Exception(f"Failed to write config to file {target_path}: {e}")
