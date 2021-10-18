from typing import Any

import magic

JPG = 'image/jpeg'
GIF = 'image/gif'
TIFF = 'image/tiff'
PNG = 'image/png'
SVG = 'image/swg+xml'
DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
XLS = ''
PDF = 'application/pdf'
TXT = 'text/plain'

ALLOWED_FORMATS = {JPG, GIF, TIFF, PNG, SVG, DOCX, XLS, PDF, TXT}


def format_validator(value: Any) -> bool:
    file = value.read(2048)
    file_type = magic.from_buffer(file, mime=True)
    print(file_type)
    return file_type in ALLOWED_FORMATS
