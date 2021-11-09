from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.accounts.serializers.user_serializer import UserSerializer
from src.apps.base.services.responses import OkResponse
from src.apps.base.services.std_error_handler import BadRequestError


class UserProfileView(GenericAPIView):

    @login_required
    def get(self, request: Request, *args: Any, user: User, **kwargs: Any) -> OkResponse:
        serializer = UserSerializer(user)
        return OkResponse(serializer.data)

    @login_required
    def put(self, request: Request, *args: Any, user: User, **kwargs: Any) -> OkResponse:
        if User.objects.filter(email=request.data.get('email')).exists():
            raise BadRequestError('This email already exists')
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)
        serializer.save()
        return OkResponse(serializer.data)
