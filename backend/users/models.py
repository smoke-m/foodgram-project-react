from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.validators import validate_name, validate_username


class User(AbstractUser):
    """Модель поьзователя."""
    username = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator()),
        verbose_name='Никнейм',
        help_text='Введите никнейм',
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_LENGTH,
        validators=(validate_name,),
        verbose_name='Фамилия',
        help_text='Введите фамилию',
    )
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_LENGTH,
        validators=(validate_name,),
        verbose_name='Имя',
        help_text='Введите имя',
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        verbose_name='электронная почта',
        help_text='Введите электронную почту',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    """Модель для создания подписок на автора."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Автор',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='уникальность_подписки'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='защита_подписки_на_себя',
            ),
        ]

    def __str__(self):
        return f'Подписчик {self.user}, Автор {self.author}'
