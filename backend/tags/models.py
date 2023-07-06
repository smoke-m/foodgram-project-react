from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from api.validators import validate_name


class Tag(models.Model):
    """Модель для  Tag."""
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        validators=(validate_name,),
        unique=True,
        verbose_name='Название тэга',
        help_text='Введите название тэга',
    )
    slug = models.SlugField(
        max_length=settings.SLAG_LENGTH,
        unique=True,
        verbose_name='Уникальный слаг',
        help_text='Введите название слага',
    )
    color = models.CharField(
        max_length=settings.COLOR_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{3,6})$',
                message='Значение не цвет в формате HEX!'
            )
        ],
        default='#E26C2D',
        verbose_name='Цвет',
        help_text='Введите например, #E26C2D',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
