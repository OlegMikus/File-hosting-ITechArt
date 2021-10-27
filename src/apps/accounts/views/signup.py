from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.accounts.serializers import UserSignUpSerializer
from src.apps.base.services.std_error_handler import BadRequestError
from src.apps.base.services.responses import CreatedResponse


class UserSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)

        serializer.save()
        return CreatedResponse(serializer.data)
