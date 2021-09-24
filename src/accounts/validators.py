import re

from django.core.exceptions import ValidationError


def validate_age(value: int) -> None:
    if not 5 < value < 110:
        raise ValidationError(
            f'{value} cannot be an age',
        )


def validate_name(value: str) -> None:
    regex = r"^[a-zA-z]+$"
    if re.match(regex, value):
        raise ValidationError(
            f'{value} is not valid phrase'
        )
