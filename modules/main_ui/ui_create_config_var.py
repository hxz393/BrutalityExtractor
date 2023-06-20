from typing import Any, Union
from functools import partial
import logging
import ttkbootstrap as ttk

from modules.main_ui import ui_on_option_change

logger = logging.getLogger(__name__)


# noinspection PyTypeChecker
def ui_create_config_var(value: Any, config_key: str) -> Union[ttk.StringVar, ttk.DoubleVar, ttk.IntVar, None]:
    """
    创建配置变量，并添加值改变时的追踪回调函数。

    :param value: 配置变量的初始值，可以是字符串、整数或浮点数。
    :type value: Any
    :param config_key: 配置项的键。
    :type config_key: str
    :rtype: Union[ttk.StringVar, ttk.DoubleVar, ttk.IntVar, None]
    :return: 创建的配置变量，类型根据值的类型确定。如果出错，则返回 None。
    """

    config_variable = None

    try:
        if isinstance(value, int):
            config_variable = ttk.IntVar(value=value)
        elif isinstance(value, float):
            config_variable = ttk.DoubleVar(value=value)
        elif isinstance(value, str):
            config_variable = ttk.StringVar(value=value)
        else:
            raise ValueError(f"Unsupported type '{type(value).__name__}' for configuration value.")

        config_variable.trace_add("write", partial(ui_on_option_change, config_key=config_key, config_var=config_variable))
    except Exception as e:
        logger.error(f"An error occurred while creating the configuration variable: {e}")

    return config_variable
