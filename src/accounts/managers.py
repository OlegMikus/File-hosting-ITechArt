from typing import Any
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where username is the unique identifier
    """
    def create_user(self, username: str, password: str, **extra_fields: Any) -> Any:
        """
        Create and save a User with the given username and password.
        """
        extra_fields.setdefault('is_alive', True)
        if not username:
            raise ValueError('The Username must be set')
        user: Any = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, password: str, **extra_fields: Any) -> Any:
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)
