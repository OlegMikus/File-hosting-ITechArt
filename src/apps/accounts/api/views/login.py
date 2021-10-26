from datetime import datetime, timedelta
from typing import Tuple

import jwt
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.api.serializers.login_serializer import UserLoginSerializer
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.base.services.responses import OkResponse
from src.config.env_consts import DJANGO_SECRET_KEY


def create_tokens(user_id: str) -> Tuple[str, str]:
    access_token = jwt.encode({
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=180),
    },
        DJANGO_SECRET_KEY)
    refresh_token = jwt.encode({
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30),
    },
        DJANGO_SECRET_KEY)

    return access_token, refresh_token


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request: Request) -> OkResponse:

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)
        access_token, refresh_token = create_tokens(serializer.data.get('id'))

        response = {
            'id': serializer.data.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return OkResponse(response)
