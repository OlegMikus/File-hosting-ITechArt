from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.accounts.validators import validate_password


class ChangePasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_repeat = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_repeat = attrs.get('new_password_repeat')

        user = self.context.get('user')
        if not user:
            raise ValidationError('User not found')
        if not user.check_password(old_password):
            raise ValidationError('Wrong password')
        if new_password != new_password_repeat:
            raise ValidationError('Passwords do not match')
        return attrs
