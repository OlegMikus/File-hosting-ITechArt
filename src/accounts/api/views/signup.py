from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.accounts.api.serializers.signup_serializer import UserSignUpSerializer
from src.base.services.std_error_handler import BadRequestError
from src.base.services.responses import CreatedResponse


class UserSignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequestError(serializer.errors)

        serializer.save()
        print(serializer.data.keys())
        return CreatedResponse(serializer.data)
