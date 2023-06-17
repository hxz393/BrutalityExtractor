from typing import Union


def format_size(size: Union[int, float], is_disk: bool = False, precision: int = 2) -> str:
    """
    将字节单位的文件或磁盘大小转换为易于理解的格式（KB, MB, GB等）。

    :type size: Union[int, float]
    :param size: 文件或磁盘的大小，单位为字节。
    :type is_disk: bool
    :param is_disk: 是否是磁盘大小（如果是磁盘大小，则使用1000作为单位换算，否则使用1024）。
    :type precision: int
    :param precision: 转换后的数值的精度（小数点后的位数）。
    :rtype: str
    :return: 格式化后的文件或磁盘大小（字符串格式）。
    :raise TypeError: 如果输入的大小不是浮点数或整数，抛出 TypeError。
    :raise ValueError: 如果输入的大小是负数，抛出 ValueError。
    """
    if not isinstance(size, (float, int)):
        raise TypeError(f"Size should be float or int, but got {type(size)}")
    if size < 0:
        raise ValueError(f"Size should not be negative, but got {size}")

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_step = 1000 if is_disk else 1024
    for unit in units:
        if abs(size) < unit_step:
            return f"{size:.{precision}f} {unit}"
        size /= unit_step

    return f"{size:.{precision}f} {units[-1]}"


def calculate_transfer_speed(size_bytes: int, elapsed_time_seconds: Union[int, float]) -> str:
    """
    根据传输的字节数和消耗的时间，计算文件传输速度并以易读的格式返回。

    :type size_bytes: int
    :param size_bytes: 传输的字节数。
    :type elapsed_time_seconds: Union[int, float]
    :param elapsed_time_seconds: 消耗的时间，单位是秒。
    :rtype: str
    :return: 文件传输速度的字符串格式，例如 "23.4 MB/s"。
    :raise TypeError: 如果输入的字节数不是整数或输入的时间不是浮点数或整数，抛出 TypeError。
    :raise ValueError: 如果输入的字节数或时间是负数或零，抛出 ValueError。
    """
    if not isinstance(size_bytes, int):
        raise TypeError(f"Size_bytes should be int, but got {type(size_bytes)}")
    if not isinstance(elapsed_time_seconds, (int, float)):
        raise TypeError(f"Elapsed_time_seconds should be int or float, but got {type(elapsed_time_seconds)}")
    if size_bytes < 0:
        raise ValueError(f"Size_bytes should not be negative, but got {size_bytes}")
    if elapsed_time_seconds <= 0:
        raise ValueError(f"Elapsed_time_seconds should be positive, but got {elapsed_time_seconds}")

    speed = size_bytes / elapsed_time_seconds

    units = ["Bytes", "KB", "MB", "GB", "TB"]
    for unit in units:
        if speed < 1024:
            return f"{speed:.2f} {unit}/s"
        speed /= 1024

    return f"{speed:.2f} {units[-1]}/s"
