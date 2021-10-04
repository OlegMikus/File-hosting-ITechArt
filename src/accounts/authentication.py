from typing import Any

import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response

from src.config.env_consts import DJANGO_SECRET_KEY


class SafeJWTAuthentication(BaseAuthentication):
    User = get_user_model()

    def authenticate(self, request: Any) -> Any:

        access_token = request.headers.get('access_token')

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

        user = self.User.objects.filter(id=payload['id']).first()

        response = {
            'success': 'False',
            'status code': status.HTTP_401_UNAUTHORIZED,
            'message': 'User is inactive or not found',
            'redirect': 'http:0.0.0.0:8000/api/login'
        }

        if user is None or not user.is_active:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        return user, None
