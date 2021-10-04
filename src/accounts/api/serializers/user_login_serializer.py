from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from src.accounts.models.user import User


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def validate(self, attrs: Any) -> Any:
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User with this email and password is not found'
            )
        try:
            update_last_login(None, user)
        except Exception as validation_error:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            ) from validation_error

        return {
            'id': user.id,
            'email': user.email
        }