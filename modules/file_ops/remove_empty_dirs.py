import logging
import os
import stat
from typing import Union, List, Optional

logger = logging.getLogger(__name__)


def remove_empty_dirs(target_path: Union[str, os.PathLike]) -> Optional[List[str]]:
    """
    删除指定路径下搜索到的所有空目录，并返回被删除的目录路径列表。

    :param target_path: 需要处理的目录路径，可以是字符串或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :return: 成功时返回一个列表，包含所有被删除的空目录的路径，如果遇到错误则返回None。
    :rtype: Optional[List[str]]
    """
    removed_dirs = []

    try:
        entries = list(os.scandir(target_path))
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                removed_dirs.extend(remove_empty_dirs(entry.path))
        if not entries:
            os.chmod(target_path, stat.S_IWRITE)
            os.rmdir(target_path)
            removed_dirs.append(str(target_path))
    except FileNotFoundError:
        logger.error(f"The path '{target_path}' does not exist.")
        return None
    except NotADirectoryError:
        logger.error(f"'{target_path}' is not a valid directory.")
        return None
    except OSError as e:
        logger.error(f"Cannot delete directory '{target_path}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while deleting empty directories: {e}")
        return None

    return removed_dirs
