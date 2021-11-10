from rest_framework.exceptions import ValidationError

from src.apps.accounts.validators import validate_age, validate_name, validate_password, username_validator


class TestValidators:
    def test_age_validator(self) -> None:
        assert validate_age(50) is None

    def test_false_age_validator(self) -> None:
        try:
            validate_age(150)
        except ValidationError:
            assert True

    def test_name_validator(self) -> None:
        assert validate_name('Test_name') is None

    def test_false_name_validator(self) -> None:
        try:
            validate_name('Name1')
        except ValidationError:
            assert True

    def test_password_validator(self) -> None:
        assert validate_password('A1@qwertyuio') is None

    def test_false_password_validator(self) -> None:
        try:
            validate_password('password')
        except ValidationError:
            assert True

    def test_username_validator(self) -> None:
        assert username_validator('Username@.+-_') is None

    def test_false_username_validator(self) -> None:
        try:
            username_validator('User$%$name')
        except ValidationError:
            assert True
