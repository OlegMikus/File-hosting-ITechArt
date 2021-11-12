from typing import Callable

import pytest
from rest_framework.exceptions import ValidationError

from src.apps.accounts.serializers.change_password_serializer import ChangePasswordSerializer
from src.apps.accounts.serializers.login_serializer import UserLoginSerializer
from src.apps.base.services.std_error_handler import BadRequestError


@pytest.mark.django_db
class TestLoginSerializer:

    def test_login_serializer(self, create_user: Callable) -> None:
        data = {'id': create_user().id, 'username': create_user().username, 'password': 'Afe3#@vdfvrrcvs'}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid() is True

    def test_login_serializer_with_invalid_email(self, create_user: Callable) -> None:
        data = {'id': create_user().id, 'username': 'username', 'password': 'Afe3#@vdfvrrcvs'}
        serializer = UserLoginSerializer(data=data, context={'user': create_user})
        with pytest.raises(BadRequestError):
            serializer.is_valid()


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_change_password_serializer(self, create_user: Callable) -> None:
        data = {'old_password': 'Afe3#@vdfvrrcvs',
                'new_password': 'Afestht3#@vdfvs',
                'new_password_repeat': 'Afestht3#@vdfvs'}
        serializer = ChangePasswordSerializer(data=data, context={'user': create_user()})
        assert serializer.is_valid() is True

    def test_change_password_serializer_with_not_matched_new_passwords(self, create_user: Callable) -> None:
        data = {'old_password': 'Afe3#@vdfvrrcvs',
                'new_password': 'Afdstht3#@vdfvs',
                'new_password_repeat': 'Afestht3#@vdfvs'}
        serializer = ChangePasswordSerializer(data=data, context={'user': create_user()})
        assert serializer.is_valid() is False
        assert 'Passwords do not match' in serializer.errors['non_field_errors']

    def test_change_password_serializer_with_invalid_old_password(self, create_user: Callable) -> None:
        data = {'old_password': 'Afe3#@vdcvs',
                'new_password': 'Afestht3#@vdfvs',
                'new_password_repeat': 'Afestht3#@vdfvs'}
        serializer = ChangePasswordSerializer(data=data, context={'user': create_user()})
        assert serializer.is_valid() is False
        assert 'Wrong password' in serializer.errors['non_field_errors']