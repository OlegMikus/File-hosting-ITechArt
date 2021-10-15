from typing import Any

import magic

ALLOWED_FORMATS = {}


def format_validator(value: Any) -> bool:
    file = value.read(2048)
    file_type = magic.from_buffer(file, mime=True)
    print(file_type)
    return file_type in ALLOWED_FORMATS
