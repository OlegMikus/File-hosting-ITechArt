from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.accounts.api.serializers.user_login_serializer import UserLoginSerializer
from src.config.env_consts import DJANGO_SECRET_KEY


def create_tokens(data) -> dict:
    access_token = jwt.encode({
        'user_id': data.get('id'),
        'user_email': data.get('email'),
        'exp': datetime.utcnow() + timedelta(seconds=180),
    },
        DJANGO_SECRET_KEY)
    refresh_token = jwt.encode({
        'user_id': data.get('id'),
        'user_email': data.get('email'),
        'exp': datetime.utcnow() + timedelta(days=30),
    },
        DJANGO_SECRET_KEY)

    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return tokens


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = create_tokens(request.data)

        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token')
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
