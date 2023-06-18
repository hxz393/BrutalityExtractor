from pathlib import Path
import configparser
import logging
from typing import Dict, Any, Union, Optional

logger = logging.getLogger(__name__)


def config_write(target_path: Union[str, Path], config: Dict[str, Union[str, Any]]) -> Optional[bool]:
    """
    将配置字典写入配置文件。

    :param target_path: 配置文件的路径。
    :type target_path: Union[str, Path]
    :param config: 配置字典，其中键为节名，值为包含该节配置项的字典。
    :type config: Dict[str, Any]
    :return: 如果文件成功写入，返回 True；如果写入失败，返回 None。
    :rtype: Optional[bool]
    """
    try:
        if not target_path:
            logger.error("Path should not be empty.")
            return None
        if not config:
            logger.error("Config should not be empty.")
            return None

        config_parser = configparser.ConfigParser()

        for section, section_config in config.items():
            config_parser[section] = {k: str(v) for k, v in section_config.items()}

        path = Path(target_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding="utf-8") as f:
            config_parser.write(f)

        return True
    except Exception as e:
        logger.error(f"Failed to write config to file {target_path}: {e}")
        return None
