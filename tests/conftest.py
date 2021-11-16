import os
import uuid
from typing import Any, Callable

import pytest

from src.apps.accounts.models import User
from src.apps.accounts.views.login import create_tokens
from src.apps.files.models import File, FilesStorage
from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def create_user() -> Callable:
    def make_user(**kwargs: Any) -> User:
        username = kwargs.pop('username', 'username')
        password = kwargs.pop('password', 'Afe3#@vdfvrrcvs')
        email = kwargs.pop('email', 'test@gmail.com')
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
            **kwargs
        )

    return make_user


@pytest.fixture
def create_token_for_user() -> Callable:
    def make_token(user: User) -> str:
        token, refresh_token = create_tokens(user_id=str(user.id))
        return token

    return make_token


@pytest.fixture
@pytest.mark.django_db
def create_file() -> Callable:
    def make_file(user: User) -> File:
        File.objects.create(user=user,
                            storage=FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT),
                            destination=os.path.join(str(user.id), 'file.txt'),
                            name='file.txt', type='text/plain',
                            size=321351, hash='dkigfbdgkfl43rfldfbd'
                            )
        return File.objects.filter(name='file.txt').first()

    return make_file
