import logging
import datetime
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
import os

DEFAULT_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s::%(funcName)s - %(message)s'


def configure_logging(log_file: bool = True, console_output: bool = False, log_level: str = 'INFO', max_log_size: int = 10, backup_count: int = 10):
    """
    配置日志记录器

    :param log_file: 是否保存日志文件
    :param console_output: 是否在控制台上输出日志
    :param log_level: 日志等级
    :param max_log_size: 最大日志文件大小（MB）
    :param backup_count: 保留的备份日志文件数量
    :return: 日志记录器
    """

    logger = getLogger(__name__)
    log_level = getattr(logging, log_level.upper())
    logger.setLevel(log_level)
    formatter = Formatter(DEFAULT_LOG_FORMAT)

    if console_output:
        ch = StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_file:
        # current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # log_file = f"logs/log_{current_date}.log"
        log_file = f"logs/Player.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        fh = RotatingFileHandler(log_file, maxBytes=max_log_size * 1024 * 1024, backupCount=backup_count)
        fh.close()
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
