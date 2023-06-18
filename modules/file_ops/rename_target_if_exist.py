import logging
from typing import Union
from pathlib import Path

logger = logging.getLogger(__name__)


def rename_target_if_exist(path: Union[str, Path]) -> Union[Path, None]:
    """
    如果目标路径存在，则重命名。

    :param path: 需要重命名的路径
    :type path: Union[str, Path]
    :return: 重命名后的路径，如果遇到错误则返回 None。
    :rtype: Union[Path, None]
    """
    try:
        if not isinstance(path, Path):
            path = Path(path)

        if path is None or str(path).strip() == '':
            logger.error("The path is empty or invalid.")
            return None

        original_path = path
        counter = 1
        while path.exists():
            path = original_path.with_stem(f"{original_path.stem}_({counter})")
            counter += 1

        return path
    except Exception as e:
        logger.error(f"An error occurred while renaming the target: {e}")
        return None
