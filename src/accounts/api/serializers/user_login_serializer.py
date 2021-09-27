from datetime import datetime, timedelta

import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from src.accounts.models.user import User
from src.config.env_consts import DJANGO_SECRET_KEY


def create_tokens(data) -> dict:
    access_token = jwt.encode({
        'user_id': data.get('id'),
        'user_email': data.get('email'),
        'exp': datetime.utcnow() + timedelta(seconds=180),
    },
        DJANGO_SECRET_KEY)
    refresh_token = jwt.encode({
        'user_id': data.get('id'),
        'user_email': data.get('email'),
        'exp': datetime.utcnow() + timedelta(days=30),
    },
        DJANGO_SECRET_KEY)

    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return tokens


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'access_token', 'password', 'refresh_token')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User with this email and password is not found'
            )
        try:
            tokens = create_tokens(data)

            access_token = tokens['access_token']
            refresh_token = tokens['refresh_token']
            update_last_login(None, user)
        except Exception:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'id': user.id,
            'email': user.email,
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
