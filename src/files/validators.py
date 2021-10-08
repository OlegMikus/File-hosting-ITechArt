import os

from django.core.exceptions import ValidationError


def file_type_validator(value: str) -> None:
    allowed_file_formats = ('.jpg', '.gif', '.tiff', '.png', '.svg', '.docx', '.xls', '.pdf', '.txt')
    if os.path.splitext(value)[1] not in allowed_file_formats:
        raise ValidationError(
            'Unsupported format, select one of the following: jpg, gif, tiff, png, svg, docx, xls, pdf, txt')
