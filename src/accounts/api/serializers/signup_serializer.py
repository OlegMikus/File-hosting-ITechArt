from typing import Any, Dict

from rest_framework import serializers

from src.accounts.models.user import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'age', 'password',)

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User.objects.create_user(**validated_data)
        return user
