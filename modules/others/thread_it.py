import logging
from threading import Thread
from typing import Any, Callable, Optional, Tuple

# 初始化日志记录器
logger = logging.getLogger(__name__)


def thread_it(func: Callable[..., Any], *args: Any, daemon: Optional[bool] = True, name: Optional[str] = None) -> None:
    """
    在新的线程中运行函数。

    :param func: 需要在新线程中运行的函数。
    :type func: Callable[..., Any]
    :param args: 函数的参数，可以是任意类型。
    :type args: Any
    :param daemon: 是否为后台线程，默认为 True。
    :type daemon: Optional[bool]
    :param name: 新线程的名字，如果没有指定，则默认为 None。
    :type name: Optional[str]
    :return: 无返回值
    :rtype: None
    :raise: 不会抛出异常，所有异常都被记录到日志中。
    """

    # noinspection PyShadowingNames
    def wrapper(*args: Tuple[Any]) -> None:
        try:
            func(*args)
        except Exception as e:
            logger.error(f"Error occurred in thread {name}: {e}")

    t = Thread(target=wrapper, args=args, daemon=daemon, name=name)
    t.start()
