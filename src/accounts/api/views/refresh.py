from typing import Any

import jwt
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.accounts.api.views.login_view import create_tokens
from src.config.env_consts import DJANGO_SECRET_KEY


class RefreshView(GenericAPIView):

    permission_classes = (AllowAny,)
    User = get_user_model()

    def get(self, request: Any) -> Response:

        refresh_token = request.headers.get('refresh_token')
        if not refresh_token:
            response = {
                'success': 'False',
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'Authentication credentials were not provided.',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        try:
            payload = jwt.decode(
                refresh_token, DJANGO_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as expired_signature:
            response = {
                'success': 'False',
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'Refresh token expired',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            raise AuthenticationFailed(response) from expired_signature
        except jwt.InvalidTokenError as invalid_token:
            response = {
                'success': 'False',
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'Invalid token',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            raise AuthenticationFailed(response) from invalid_token

        user = self.User.objects.filter(id=payload.get('id')).first()

        if user is None:
            response = {
                'success': 'False',
                'status code': status.HTTP_401_UNAUTHORIZED,
                'message': 'User not found',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            response = {
                'success': 'False',
                'status code': status.HTTP_401_UNAUTHORIZED,
                'message': 'User is inactive',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        tokens = create_tokens(payload)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'IF U see this, than your token was refresh correctly',
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token')
        }

        return Response(response, status=status.HTTP_200_OK)
