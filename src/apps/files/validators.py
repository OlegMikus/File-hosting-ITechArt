from typing import Any

import magic

from src.apps.files.constants import ALLOWED_FORMATS


def format_validator(value: Any) -> bool:
    file = value.read(1024)
    file_type = magic.from_buffer(file, mime=True)
    return file_type in ALLOWED_FORMATS
