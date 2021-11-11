from functools import wraps
from typing import Any
import jwt

from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import BadRequestError, ForbiddenError
from src.config.env_consts import DJANGO_SECRET_KEY


def login_required(func: Any) -> Any:
    @wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        access_token = args[1].headers.get('Access-Token')

        if not access_token:
            raise BadRequestError('Missing token')
        try:
            payload = jwt.decode(
                access_token, DJANGO_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload.get('id')).first()
            if user and user.is_active:
                return func(user=user, *args, **kwargs)

        except jwt.ExpiredSignatureError as expired_signature:
            raise ForbiddenError(expired_signature.args[0]) from expired_signature
        except jwt.InvalidSignatureError as invalid_signature:
            raise ForbiddenError(invalid_signature.args[0]) from invalid_signature
    return decorated
