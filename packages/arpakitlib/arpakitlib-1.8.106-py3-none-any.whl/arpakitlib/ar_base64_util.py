# arpakit

import base64
from typing import Optional

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def convert_base64_string_to_bytes(base64_string: str, raise_for_error: bool = False) -> Optional[bytes]:
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        if raise_for_error:
            raise e
        return None


def convert_bytes_to_base64_string(bytes_: bytes, raise_for_error: bool = False) -> Optional[str]:
    try:
        return base64.b64encode(bytes_).decode()
    except Exception as e:
        if raise_for_error:
            raise e
        return None


def __example():
    pass


if __name__ == '__main__':
    __example()
