import uuid

from django.db import models


class BaseModel(models.Model):
    """
    An abstract base class implementing a base fields for all models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    """
    Class that implementing user entity

    All fields are required
    """
    first_name = models.CharField(max_length=30,
                                  help_text='Users first name')

    last_name = models.CharField(max_length=40,
                                 help_text='Users last name')

    email = models.EmailField(max_length=254,
                              unique=True,
                              help_text='Users email')

    age = models.IntegerField(help_text='')

    password = models.CharField(max_length=64,
                                help_text='Users password')

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
