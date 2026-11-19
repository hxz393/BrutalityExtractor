import logging
import os
from typing import Optional, Union

logger = logging.getLogger(__name__)


def _detect_from_signature(header: bytes) -> Optional[str]:
    if header.startswith(b'7z\xbc\xaf\x27\x1c'):
        return 'application/x-7z-compressed'
    if header.startswith(b'PK\x03\x04') or header.startswith(b'PK\x05\x06') or header.startswith(b'PK\x07\x08'):
        return 'application/zip'
    if header.startswith(b'Rar!\x1a\x07\x00') or header.startswith(b'Rar!\x1a\x07\x01\x00'):
        return 'application/x-rar'
    if header.startswith(b'\x1f\x8b'):
        return 'application/x-gzip'
    if header.startswith(b'\xfd7zXZ\x00'):
        return 'application/x-xz'
    if header.startswith(b'BZh'):
        return 'application/x-bzip2'
    if len(header) >= 262 and header[257:262] == b'ustar':
        return 'application/x-tar'
    return None


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
            header = f.read(1024)

        signature_type = _detect_from_signature(header)
        if signature_type:
            return signature_type

        try:
            import magic
            return magic.from_buffer(header, mime=True)
        except (ImportError, AttributeError, OSError):
            return _detect_from_signature(header)
    except PermissionError:
        logger.error(f"Unable to access file '{target_path}', permission denied.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while detecting the file type: {e}")
        return None
