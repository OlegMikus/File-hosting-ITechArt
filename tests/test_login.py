import pytest

from src.apps.accounts.models import User


@pytest.mark.django_db
class TestModels:

    def test_user_creation(self) -> None:
        User.objects.create_user(username='test_user', email='testuser@test.com',
                                 first_name='test_name',
                                 password='Admin@12432')
        assert User.objects.count() == 1

    def test_user_deletion(self) -> None:
        User.objects.create_user(username='test_user', email='testuser@test.com',
                                 first_name='test_name',
                                 password='Admin@12432')
        user = User.objects.get(username='test_user')
        user.delete()
        assert user.is_alive is False
