from modules.conf_init import LANG

def format_size(size, is_disk=False, precision=2) -> str:
    """
    转换文件大小单位

    :param size: 文件大小（字节数）
    :param is_disk: 是否是磁盘大小（使用1000作为单位换算）
    :param precision: 精度
    :return: 格式化后的文件大小
    """
    format_list = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1000.0 if is_disk else 1024.0

    if not isinstance(size, (float, int)):
        raise TypeError(LANG["format_size_typeerror"])
    if size < 0:
        raise ValueError(LANG["format_size_valueerror"])

    for fmt in format_list:
        size, remainder = divmod(size, unit)
        if size < unit:
            return f'{round(size, precision)} {fmt}'


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
        raise ValueError("format_size_valueerror")

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
