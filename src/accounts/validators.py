import re

from django.core.exceptions import ValidationError


def validate_age(value: int) -> None:
    if not 5 < value < 110:
        raise ValidationError(
            f'{value} cannot be an age',
        )


def validate_name(value: str) -> None:
    regex = r"^[a-zA-z]+$"
    if not re.match(regex, value):
        raise ValidationError(
            f'{value} is not valid phrase'
        )


def validate_password(value: str) -> bool:
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,20}$'
    if not re.match(regex, value):
        raise ValidationError(
            f'{value} is not valid password'
        )
    return True
