from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=settings.USERNAME_LENGTH, unique=True,
        validators=(validate_username, UnicodeUsernameValidator()))
    last_name = models.CharField(
        max_length=settings.LAST_NAME_LENGTH, blank=True)
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_LENGTH, blank=True)
    email = models.EmailField(max_length=settings.EMAIL_LENGTH, unique=True,
                              blank=False, null=False)

    class Meta:
        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    """ Модель для создания подписок на автора."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow',
            ),
        ]

    def __str__(self):
        return f'Подписчик {self.user}, Автор {self.author}'
