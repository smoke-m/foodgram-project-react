from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Модель юзера."""
    USER = 'user'
    ADMIN = 'admin'
    ROLE = [
        (USER, 'пользователь'),
        (ADMIN, 'админ'),
    ]
    username = models.CharField(
        max_length=settings.USERNAME_LENGTH, unique=True,
        validators=(validate_username, UnicodeUsernameValidator())
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_LENGTH, blank=True)
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_LENGTH, blank=True)
    email = models.EmailField(max_length=settings.EMAIL_LENGTH, unique=True,
                              blank=False, null=False)
    role = models.CharField(max_length=settings.ROLE_LENGTH,
                            choices=ROLE, default=USER)

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f'{self.username} {self.email} {self.role}'
