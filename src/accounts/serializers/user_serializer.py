from rest_framework.serializers import ModelSerializer

from src.accounts.models.user import User


class UserSerializer(ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age', )
