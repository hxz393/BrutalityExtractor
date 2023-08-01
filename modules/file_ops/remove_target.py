import logging
import traceback
import os
import shutil
import stat
from pathlib import Path
from typing import Callable, Any, Union, Optional

logger = logging.getLogger(__name__)


def remove_permissions(func: Callable[[Path], Any], path: Path, _: Any) -> None:
    """
    移除目标路径的权限并调用指定的函数。

    :param func: 要调用的函数。
    :type func: Callable[[Path], Any]
    :param path: 目标路径。
    :type path: Path
    :param _: 用于异常处理的错误信息。
    :type _: Any
    """
    # path.chmod(0o777)
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_target(path: Union[str, Path]) -> Optional[Path]:
    """
    删除指定文件或目录。

    :param path: 要删除的文件或目录的路径。
    :type path: Union[str, Path]
    :return: 如果操作成功则返回删除的文件或目录的路径，遇到错误则返回 None。
    :rtype: Optional[Path]
    """
    path = Path(path)

    try:
        if not path.exists():
            logger.error(f"Path '{path}' does not exist.")
            return None

        if path.is_dir():
            shutil.rmtree(path, onerror=remove_permissions)
            return path
        elif path.is_file():
            path.unlink()
            return path
        else:
            logger.error(f"'{path}' is neither a file nor a directory.")
            return None
    except PermissionError:
        remove_permissions(lambda x: None, path, None)
        path.unlink()
        return path
    except Exception as e:
        logger.error(f"An error occurred while removing path '{path}': {e}\n{traceback.format_exc()}")
        return None
