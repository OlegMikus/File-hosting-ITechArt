from functools import wraps
from typing import Any
import jwt
from rest_framework.request import Request

from src.accounts.models import User
from src.base.services.std_error_handler import BadRequestError, ForbiddenError
from src.config.env_consts import DJANGO_SECRET_KEY


def login_required(func: Any) -> Any:
    @wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        access_token = None
        for arg in args:
            if isinstance(arg, Request):
                access_token = arg.headers.get('Access-Token')

        if not access_token:
            raise BadRequestError('Missing token')
        try:
            payload = jwt.decode(
                access_token, DJANGO_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload.get('id')).first()

            if user and user.is_active:
                return func(*args, **kwargs)

        except jwt.ExpiredSignatureError as expired_signature:
            raise ForbiddenError(expired_signature) from expired_signature
        except jwt.InvalidSignatureError as invalid_signature:
            raise ForbiddenError(invalid_signature) from invalid_signature
    return decorated
