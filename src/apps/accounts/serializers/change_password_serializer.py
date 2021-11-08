from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.accounts.models import User
from src.apps.accounts.validators import validate_password
from src.apps.base.services.std_error_handler import BadRequestError


class ChangePasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_repeat = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_repeat = attrs.get('new_password_repeat')

        if not self.context.check_password(old_password):
            raise ValidationError('Wrong password')
        if new_password != new_password_repeat:
            raise ValidationError('passwords do not match')
        return attrs
