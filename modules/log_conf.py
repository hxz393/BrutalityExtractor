import logging
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

from modules.conf_init import DEFAULT_LOG_FORMAT


def configure_logging(log_file: Optional[str] = None, console_output: bool = False, log_level: str = 'INFO',
                      max_log_size: int = 10, backup_count: int = 10) -> logging.Logger:
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
    :raise ValueError: 当日志等级不在可接受的日志等级列表中时抛出
    :return: 配置好的日志记录器
    :rtype: logging.Logger
    """
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    if log_level.upper() not in log_levels:
        raise ValueError(f"无效的日志等级: {log_level}，必须是 {log_levels} 中的一种")

    logger = getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    formatter = Formatter(DEFAULT_LOG_FORMAT)

    if console_output:
        ch = StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        fh = RotatingFileHandler(log_file, maxBytes=max_log_size * 1024 * 1024, backupCount=backup_count, encoding="utf-8")
        fh.close()
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
