from rest_framework.serializers import ModelSerializer

from src.apps.accounts.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'age')
        read_only_fields = ('username', )
