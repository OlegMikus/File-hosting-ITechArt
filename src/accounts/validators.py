from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_age(value: int) -> None:

    if value < 5 or value > 110:

        raise ValidationError(
            _(f'{value} cannot be an age'),
            params={'value': value},
        )


def validate_name(value: str) -> None:

    allowed = 'abcdefghijklmnopqrstuvwxyz'
    for symbol in value:
        if symbol.lower() not in allowed:

            raise ValidationError(
                _(f'{value} cannot be an age'),
                params={'value': value},
            )
