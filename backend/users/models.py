from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.validators import validate_username, validate_name


class User(AbstractUser):
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
        verbose_name='email',
        help_text='Введите email',
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    """ Модель для создания подписок на автора."""
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
