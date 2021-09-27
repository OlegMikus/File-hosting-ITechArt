from rest_framework import serializers

from src.accounts.models.user import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
