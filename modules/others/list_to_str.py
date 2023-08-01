import logging
import traceback
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


def list_to_str(a: Optional[List[Union[str, int]]]) -> Optional[str]:
    """
    将列表中的元素转换为字符串并连接在一起。元素之间用换行符("\n")分隔。

    :type a: Optional[List[Union[str, int]]]
    :param a: 输入的列表，其元素为字符串或整数。如果列表为空或为 None，将返回 None。
    :rtype: Optional[str]
    :return: 一个字符串，其中包含列表中所有元素的字符串表示形式，元素之间用换行符分隔，或者在列表为空或为 None 时返回 None。
    """
    try:
        if a:
            return "\n".join(str(element) for element in a)
        else:
            return None
    except Exception as e:
        logger.error(f"An error occurred while converting list to string: {e}\n{traceback.format_exc()}")
        return None
