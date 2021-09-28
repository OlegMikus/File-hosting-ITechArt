import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from src.config.env_consts import DJANGO_SECRET_KEY


class SafeJWTAuthentication(BaseAuthentication):
    User = get_user_model()

    def authenticate(self, request):

        access_token = request.headers.get('access_token')

        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, DJANGO_SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = self.User.objects.filter(id=payload['id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return user, None
