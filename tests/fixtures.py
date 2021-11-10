import io
import os
import uuid

import pytest

from src.apps.files.models import File, FilesStorage


@pytest.fixture
def test_password():
    return 'Afe3#@vdfvrrcvs'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_token_for_user(db, create_user):
    from src.apps.accounts.views.login import create_tokens
    user = create_user()
    token, refresh_token = create_tokens(user_id=str(user.id))
    return token, user


@pytest.fixture
def create_file(db, create_token_for_user):
    from src.apps.files.constants import FILE_STORAGE__TYPE__PERMANENT
    File.objects.create(user=create_token_for_user[1],
                        storage=FilesStorage.objects.get(type=FILE_STORAGE__TYPE__PERMANENT),
                        destination=os.path.join(str(create_token_for_user[1].id), 'file.txt'),
                        name='file.txt',
                        type='text/plain',
                        size=321351,
                        hash='dkigfbdgkfl43rfldfbd'
                        )
    return File.objects.filter(name='file.txt').first()


@pytest.fixture
def create_upload_file_data():
    return {
        'file': (io.BytesIO(b"some initial text data"), 'file.txt'),
        'hash_sum': 'a2827ed8c47e1a385bbd469def62aafd',
        'description': 'test description',
        'extension': 'text/plain',
        'total_size': '234',
        'filename': 'file'
    }


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

