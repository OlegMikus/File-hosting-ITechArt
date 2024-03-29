from typing import Any
from urllib.request import Request

from rest_framework.generics import GenericAPIView

from src.apps.accounts.authentication import login_required
from src.apps.accounts.models import User
from src.apps.accounts.serializers.change_password_serializer import ChangePasswordSerializer
from src.apps.base.services.responses import OkResponse
from src.apps.base.services.std_error_handler import BadRequestError


class ChangePasswordView(GenericAPIView):

    @login_required
    def put(self, request: Request, *args: Any, user: User, **kwargs: Any) -> OkResponse:
        serializer = ChangePasswordSerializer(data=request.data, context={'user': user})
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)
        serializer.set_password()
        return OkResponse(data={})
