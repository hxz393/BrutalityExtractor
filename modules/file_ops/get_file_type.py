import logging
import os
from typing import Optional, Union

import magic

logger = logging.getLogger(__name__)


def get_file_type(target_path: Union[str, os.PathLike]) -> Optional[str]:
    """
    以读取文件头部内容的方式，取得指定文件的真实类型

    :type target_path: Union[str, os.PathLike]
    :param target_path: 要检测的文件路径，可以是字符串或 os.PathLike 对象。
    :rtype: Optional[str]
    :return: 文件类型检测结果，如果检测失败则返回 None。
    """
    try:
        target_path = os.path.normpath(target_path)
        if not os.path.exists(target_path):
            logger.error(f"The file '{target_path}' does not exist.")
            return None
        if not os.path.isfile(target_path):
            logger.error(f"'{target_path}' is not a valid file.")
            return None

        with open(target_path, 'rb') as f:
            return magic.from_buffer(f.read(1024), mime=True)
    except PermissionError:
        logger.error(f"Unable to access file '{target_path}', permission denied.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while detecting the file type: {e}")
        return None
