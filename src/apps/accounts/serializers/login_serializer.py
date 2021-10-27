from typing import Dict

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from src.apps.accounts.models.user import User
from src.apps.base.services.std_error_handler import BadRequestError


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise BadRequestError('Invalid username or password')

        update_last_login(None, user)

        return {
            'id': user.id,
            'username': user.username
        }
