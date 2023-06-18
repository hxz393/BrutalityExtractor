import configparser
from typing import Any, Callable

def config_get(config: configparser.ConfigParser, section: str, option: str, getter: Callable[[str, str], Any]) -> Any:
    """
    尝试使用指定的 getter 函数从配置中获取指定选项的值。
    如果 getter 函数引发 ValueError 异常，则尝试从 DEFAULT section 获取该选项的值。

    :param config: 配置解析器对象
    :type config: configparser.ConfigParser
    :param section: 配置中的 section 名称
    :type section: str
    :param option: 要获取的选项名称
    :type option: str
    :param getter: 用于获取值的函数
    :type getter: Callable[[str, str], Any]
    :return: 获取的配置值
    :rtype: Any
    """
    try:
        return getter(section, option)
    except ValueError:
        return getter(config.default_section, option)
