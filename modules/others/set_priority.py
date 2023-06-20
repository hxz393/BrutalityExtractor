import logging
import os
from typing import Optional

import psutil

logger = logging.getLogger(__name__)


def set_priority(pid: Optional[int] = None, priority: int = psutil.REALTIME_PRIORITY_CLASS) -> Optional[bool]:
    """
    设置指定进程的优先级。

    :param pid: 进程 ID，如果没有指定，则为当前进程。
    :type pid: Optional[int]
    :param priority: 进程优先级，默认为实时优先级。
    :type priority: int
    :rtype: Optional[bool]
    :return: 在成功设置优先级时返回 True，否则在发生错误时返回 None。
    :raise: ValueError, psutil.AccessDenied, psutil.NoSuchProcess
    """
    try:
        if pid is None:
            pid = os.getpid()

        process = psutil.Process(pid)
        process.nice(priority)
        return True

    except ValueError as ve:
        logger.error(f"An invalid priority was specified: {ve}")
    except psutil.AccessDenied as ad:
        logger.error(f"Insufficient permissions to change the priority: {ad}")
    except psutil.NoSuchProcess as nsp:
        logger.error(f"The process does not exist: {nsp}")

    return None
