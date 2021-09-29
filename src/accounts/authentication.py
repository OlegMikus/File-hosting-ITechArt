import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions, status
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
            response = {
                'success': 'False',
                'status code': status.HTTP_403_FORBIDDEN,
                'message': 'Access token expired',
                'redirect': 'http:0.0.0.0:8000/api/refresh'
            }

            raise exceptions.AuthenticationFailed(response)

        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = self.User.objects.filter(id=payload['id']).first()

        if user is None:
            response = {
                'success': 'False',
                'status code': status.HTTP_401_UNAUTHORIZED,
                'message': 'User not found',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            raise exceptions.AuthenticationFailed(response)

        if not user.is_active:
            response = {
                'success': 'False',
                'status code': status.HTTP_401_UNAUTHORIZED,
                'message': 'User is inactive',
                'redirect': 'http:0.0.0.0:8000/api/login'
            }
            raise exceptions.AuthenticationFailed(response)
        return user, None
