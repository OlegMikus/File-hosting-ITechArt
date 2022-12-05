from rest_framework.exceptions import ValidationError
import pytest

from src.apps.accounts.validators import validate_age, validate_name, validate_password, username_validator


class TestValidators:
    def test_age_validator(self) -> None:
        assert validate_age(50) is None

    def test_age_validator_fail(self) -> None:
        with pytest.raises(ValidationError):
            validate_age(150)

    def test_name_validator(self) -> None:
        assert validate_name('Test_name') is None

    def test_name_validator_fail(self) -> None:
        with pytest.raises(ValidationError):
            validate_name('Name1')

    def test_password_validator(self) -> None:
        assert validate_password('A1@qwertyuio') is None

    def test_password_validator_fail(self) -> None:
        with pytest.raises(ValidationError):
            validate_password('password')

    def test_username_validator(self) -> None:
        assert username_validator('Username@.+-_') is None

    def test_username_validator_fail(self) -> None:
        with pytest.raises(ValidationError):
            username_validator('User$%$name')
