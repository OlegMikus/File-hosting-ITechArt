from typing import Callable

import pytest

from src.apps.accounts.serializers.change_password_serializer import ChangePasswordSerializer
from src.apps.accounts.serializers.login_serializer import UserLoginSerializer
from src.apps.base.services.std_error_handler import BadRequestError


@pytest.mark.django_db
class TestLoginSerializer:

    def test_pass_when_valid_user_data(self, create_user: Callable) -> None:

        user = create_user()
        data = {'id': user.id, 'username': user.username, 'password': 'Afe3#@vdfvrrcvs'}
        serializer = UserLoginSerializer(data=data)

        assert serializer.is_valid() is True

    def test_fails_when_invalid_username(self, create_user: Callable) -> None:

        user = create_user()
        data = {'id': user.id, 'username': 'test', 'password': 'Afe3#@vdfvrrcvs'}
        serializer = UserLoginSerializer(data=data, context={'user': user})

        with pytest.raises(BadRequestError):
            serializer.is_valid()

    def test_fails_when_invalid_password(self, create_user: Callable) -> None:

        user = create_user()
        data = {'id': user.id, 'username': user.username, 'password': 'Afe3#@vdfvolbcvs'}
        serializer = UserLoginSerializer(data=data, context={'user': user})

        with pytest.raises(BadRequestError):
            serializer.is_valid()


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_pass_when_valid_data_passed(self, create_user: Callable) -> None:

        user = create_user()
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'Afe3#@vdfvrrcvs'
        }
        serializer = ChangePasswordSerializer(data=data, context={'user': user})

        assert serializer.is_valid() is True

    def test_fails_when_invalid_password(self, create_user: Callable) -> None:

        user = create_user()
        data = {
            'new_password': 'asf#423Adfwer32',
            'new_password_repeat': 'asf#423Adfwer32',
            'old_password': 'Afekjhu#@vdfvrrc'
        }
        serializer = ChangePasswordSerializer(data=data, context={'user': user})

        assert serializer.is_valid() is False

    def test_fails_when_new_passwords_do_not_match(self, create_user: Callable) -> None:

        data = {'old_password': 'Afe3#@vdfvrrcvs',
                'new_password': 'Afdstht3#@vdfvs',
                'new_password_repeat': 'Afestht3#@vdfvs'}
        serializer = ChangePasswordSerializer(data=data, context={'user': create_user()})

        assert serializer.is_valid() is False
        assert 'Passwords do not match' in serializer.errors['non_field_errors']
