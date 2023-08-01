import logging
import traceback
import os
from typing import Any

from modules.configs import CP, CONFIG_PATH
from modules.module_use import config_write

logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def ui_on_option_change(*args, config_key: str = '', config_var: Any = None) -> None:
    """
    当选项改变时，更新配置并写入文件。

    :param args: 额外的参数（未使用）。
    :type args: tuple
    :param config_key: 配置项的键。
    :type config_key: str
    :param config_var: 配置项的新值。
    :type config_var: Any
    :rtype: None
    """
    try:
        # 更新配置
        CP.set('main', config_key, str(config_var.get()))

        # 检查路径
        normalized_path = os.path.normpath(CONFIG_PATH)

        # 写入文件
        config_write(normalized_path, CP)
    except Exception as e:
        logger.error(f"An error occurred while updating configuration: {e}\n{traceback.format_exc()}")
