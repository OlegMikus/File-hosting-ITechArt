from typing import Any

import jwt
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.api.views.login import create_tokens
from src.apps.accounts.models import User
from src.apps.base.services.std_error_handler import ForbiddenError, BadRequestError
from src.apps.base.services.responses import OkResponse
from src.config.env_consts import DJANGO_SECRET_KEY


class RefreshView(GenericAPIView):
    queryset = User

    def get(self, request: Request, *args: Any, **kwargs: Any) -> OkResponse:

        refresh_token = request.headers.get('Refresh-Token')

        if not refresh_token:
            raise BadRequestError('Missing token')

        try:
            payload = jwt.decode(
                refresh_token, DJANGO_SECRET_KEY, algorithms=['HS256'])

            user = self.queryset.objects.filter(id=payload.get('id')).first()
            if not user.is_active or user is None:
                raise ForbiddenError('No such user or user is not active')

            access_token, refresh_token = create_tokens(payload.get('id'))

            response = {
                'id': payload.get('id'),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return OkResponse(response)
        except jwt.ExpiredSignatureError as expired_signature:
            raise ForbiddenError(expired_signature) from expired_signature
        except jwt.InvalidTokenError as invalid_token:
            raise ForbiddenError(invalid_token) from invalid_token
