from functools import wraps
from typing import Any
import jwt
from rest_framework import exceptions, status
from rest_framework.response import Response

from src.accounts.models import User
from src.config.env_consts import DJANGO_SECRET_KEY


def login_required(func: Any) -> Any:
    @wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Response:

        access_token = args[1].headers.get('access_token')

        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, DJANGO_SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError as expired_signature:
            response = {
                'success': 'False',
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'Access token expired',
                'redirect': 'http:0.0.0.0:8000/api/refresh'
            }
            raise exceptions.AuthenticationFailed(response) from expired_signature
        except IndexError as index_error:
            raise exceptions.AuthenticationFailed('Token prefix missing') from index_error

        user = User.objects.filter(id=payload['id']).first()
        if user and user.is_active:
            return func(*args, **kwargs)

    return decorated
