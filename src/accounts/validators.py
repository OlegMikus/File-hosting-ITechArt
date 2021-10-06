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


def validate_password(value: str) -> None:
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,20}$'
    if not re.match(regex, value):
        raise ValidationError(
            'Password must contain: more than 10 chars,'
            'at least 1 uppercase letter,'
            'at least 1 lowercase letter,'
            'at least 1 number,'
            'at least 1 special char'
        )


def username_validator(value: str) -> None:
    regex = r'^[\w.@+-]+\Z'
    if not re.match(regex, value):
        raise ValidationError(
            'Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.'
        )
