from django.contrib.auth.models import AbstractUser
from django.db import models

from src.accounts.managers import CustomUserManager
from src.base.models.base import BaseModel
from src.accounts.validators import validate_age, validate_name


class User(BaseModel, AbstractUser):
    """
    Class that implementing user entity

    All fields are required
    """
    username = None

    first_name = models.CharField(max_length=30,
                                  validators=[validate_name],
                                  blank=True,
                                  help_text='Users first name')

    last_name = models.CharField(max_length=40,
                                 validators=[validate_name],
                                 help_text='Users last name',
                                 blank=True)

    email = models.EmailField(max_length=254,
                              unique=True,
                              help_text='Users email')

    age = models.PositiveIntegerField(help_text='Users age',
                                      validators=[validate_age])

    password = models.CharField(max_length=256,
                                help_text='Users password')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f'{self.id} {self.first_name} {self.last_name}'
