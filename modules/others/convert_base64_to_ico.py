import atexit
import base64
import logging
import os
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


def remove_temp_file(path: str):
    """删除临时文件"""
    try:
        os.remove(path)
    except Exception as e:
        logger.error(f"Error when remove temp file: {e}")
        pass


def convert_base64_to_ico(base64_string: str) -> Optional[str]:
    """
    将Base64字符串解码并保存为.ico文件。

    :param base64_string: Base64编码的字符串。
    :type base64_string: str
    :return: 生成的.ico文件的路径，如果过程中有错误发生，返回 None。
    :rtype: Optional[str]
    """
    try:
        icon_data = base64.b64decode(base64_string)
    except Exception as e:
        logger.error(f"The input string cannot be decoded by Base64: {str(e)}")
        return None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ico') as temp_file:
            temp_file.write(icon_data)
        atexit.register(remove_temp_file, temp_file.name)
        return temp_file.name
    except Exception as e:
        logger.error(f"An error occurred while writing the .ico file: {str(e)}")
        return None
