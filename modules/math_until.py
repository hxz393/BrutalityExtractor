from modules.conf_init import LANG
from typing import Union

def format_size(size: Union[int, float], is_disk: bool = False, precision: int = 2) -> str:
    """
    将字节单位的文件或磁盘大小转换为易于理解的格式（KB, MB, GB等）。

    :param size: 文件或磁盘的大小，单位为字节。
    :type size: Union[int, float]
    :param is_disk: 是否是磁盘大小（如果是磁盘大小，则使用1000作为单位换算，否则使用1024）。
    :type is_disk: bool, default False
    :param precision: 转换后的数值的精度（小数点后的位数）。
    :type precision: int, default 2
    :raise TypeError: 如果输入的大小不是浮点数或整数。
    :raise ValueError: 如果输入的大小是负数。
    :return: 格式化后的文件或磁盘大小（字符串格式）。
    """
    format_list = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1000.0 if is_disk else 1024.0

    if not isinstance(size, (float, int)):
        raise TypeError(LANG["format_size_typeerror"])
    if size < 0:
        raise ValueError(LANG["format_size_valueerror"])

    for fmt in format_list:
        if size < unit:
            return f'{round(size, precision)} {fmt}'
        size /= unit


def format_time(duration: float, decimal_places: int = 2) -> str:
    """
    转换时间单位

    :param duration: 时间长度
    :param decimal_places: 小数点精度
    :return: 格式化后的时间字符串
    """
    FORMAT_LIST = [LANG["second"], LANG["minute"], LANG["hour"]]
    UNIT = 60.0

    if not (isinstance(duration, (float, int))):
        raise TypeError(LANG["format_size_typeerror"])
    if duration < 0:
        raise ValueError(LANG["format_size_valueerror"])

    for fmt in FORMAT_LIST:
        if duration < UNIT:
            return f'{round(duration, decimal_places)} {fmt}'
        else:
            duration /= UNIT

    return f'{round(duration, decimal_places)} {FORMAT_LIST[-1]}'


def calculate_speed(size_bytes: int, elapsed_time_seconds: float) -> str:
    """
    计算每秒传输的字节数

    :param size_bytes: 大小，比特
    :param elapsed_time_seconds: 花费时间，秒
    :return: 返回每秒处理速度，
    """
    bytes_per_second = size_bytes / elapsed_time_seconds

    units = ["Bytes", "KB", "MB", "GB"]
    index = 0
    while bytes_per_second >= 1024 and index < len(units) - 1:
        bytes_per_second /= 1024
        index += 1

    speed_formatted = f"{bytes_per_second:.2f} {units[index]}/{LANG['s']}"

    return speed_formatted


def is_numeric(s: str) -> bool:
    """如果是数字，返回 True 否则 False."""
    return s.isdigit() or s == ""


def is_alpha(s: str) -> bool:
    """如果是字符串，返回 True 否则 False."""
    return s.isalpha() or s == ""


def is_not_empty(s: str) -> bool:
    """如果有内容，返回 True 否则 False."""
    return s != ""
