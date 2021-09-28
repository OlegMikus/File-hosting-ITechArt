import jwt
from django.contrib.auth import get_user_model
from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from src.accounts.api.views.login_view import create_tokens
from src.config.env_consts import DJANGO_SECRET_KEY


class RefreshView(GenericAPIView):

    User = get_user_model()

    def post(self, request) -> Response:

        refresh_token = request.headers['refresh_token']
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, DJANGO_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = self.User.objects.filter(id=payload.get('id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        tokens = create_tokens(payload)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'IF U see this, than your token was refresh correctly',
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token')
        }

        return Response(response, status=status_code)
