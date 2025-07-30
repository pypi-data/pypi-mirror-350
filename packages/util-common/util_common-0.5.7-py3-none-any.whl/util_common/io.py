import base64
import json
from typing import Dict, List, Optional

import magic

from util_common.path import FileExt, guess_extension_from_mime


def json_to_str(
    json_: Dict | List | None,
    indent=4,
    ensure_ascii=False,
):
    return json.dumps(json_, indent=indent, ensure_ascii=ensure_ascii)


def json_to_bytes(
    json_: Dict | List | None,
    indent=4,
    ensure_ascii=False,
    encoding="utf-8",
) -> bytes:
    return bytes(
        json_to_str(json_, indent=indent, ensure_ascii=ensure_ascii),
        encoding=encoding,
    )


def str_to_bytes(text: str, encoding="utf-8") -> bytes:
    return bytes(text, encoding=encoding)


def bytes_to_str(content: bytes, encoding="utf-8") -> str:
    return content.decode(encoding=encoding)


def bytes_to_b64str(content: bytes, encoding="utf-8") -> str:
    return base64.b64encode(content).decode(encoding)


def b64str_to_bytes(b64str: str) -> bytes:
    return base64.b64decode(b64str)


def parse_bool(value: str | int | bool) -> bool:
    try:
        value = int(value)
    except Exception:
        pass
    if isinstance(value, bool) or isinstance(value, int):
        return bool(value)
    return value.lower().startswith("t") or value.lower().startswith("y")


def parse_int(value: str | int | float) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except Exception as e:
            raise e


def guess_file_extension(content: bytes) -> Optional[FileExt]:
    mime = magic.from_buffer(content, mime=True).lower()
    ext = guess_extension_from_mime(mime)
    return ext
