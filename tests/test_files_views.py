import pytest
from django.urls import reverse
from django.test import RequestFactory
from src.apps.accounts.models import User
from django.test import TestCase


@pytest.mark.django_db
class TestModels(TestCase):
    def setUpClass(cls):
        super(TestModels, cls).setUpClass()
        user_1 = User.objects.create_user(username='test_user', email='testuser@test.com',
                                          first_name='test_name',
                                          password='Admin@12432')
        user_2 = User.objects.create_user(username='test_user_2', email='testuser2@test.com',
                                 first_name='test_name_2',
                                 password='Admin@12432')

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

    def test_temp(self):
        path = reverse('detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user
