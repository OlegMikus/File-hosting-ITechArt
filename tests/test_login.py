import pytest

from src.apps.accounts.models import User


@pytest.mark.django_db
def test_temp() -> None:
    User.objects.create_user(username='john', email='lennon@thebeatles.com', first_name='johnpassword')
    assert User.objects.count() == 1
