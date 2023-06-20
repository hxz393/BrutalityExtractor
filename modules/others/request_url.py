import logging
from typing import Optional

import requests
import urllib3

logger = logging.getLogger(__name__)


def request_url(url: str) -> Optional[str]:
    """
    通过 HTTP GET 请求获取给定 URL 的响应内容。

    :param url: 待请求的 URL
    :type url: str

    :rtype: Optional[str]
    :return: 如果请求成功，返回 URL 的响应内容；否则返回 None
    :raise: 不抛出任何异常，而是用日志记录所有异常
    """
    session = requests.Session()
    session.trust_env = False
    urllib3.disable_warnings()

    try:
        response = session.get(url, verify=False, timeout=5)
        # 检查响应的状态码，如果不是 200，则抛出异常
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to send network request to {url}: {e}")
        return None
