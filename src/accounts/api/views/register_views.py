from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from src.accounts.api.serializers.user_register_serializer import UserRegistrationSerializer


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)
