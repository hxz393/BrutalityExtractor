from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)


def calculate_transfer_speed(size_bytes: int, elapsed_time_seconds: Union[int, float]) -> Optional[str]:
    """
    根据传输的字节数和消耗的时间，计算文件传输速度并以易读的格式返回。

    :param size_bytes: 传输的字节数。
    :type size_bytes: int
    :param elapsed_time_seconds: 消耗的时间，单位是秒。
    :type elapsed_time_seconds: Union[int, float]
    :return: 文件传输速度的字符串格式，例如 "23.4 MB/s"，若发生错误则返回 None。
    :rtype: Optional[str]
    """
    try:
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
    except Exception as e:
        logger.error(f"An error occurred while calculating transfer speed: {e}")
        return None
