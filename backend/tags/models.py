from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    """Модель для  Tag."""
    name = models.CharField(max_length=settings.NAME_LENGTH, unique=True)
    slug = models.SlugField(max_length=settings.SLAG_LENGTH, unique=True,)
    color = models.CharField(
        max_length=settings.COLOR_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Значение не цвет в формате HEX!'
            )
        ],
        default='#E26C2D',
        help_text='Введите например, #E26C2D',
    )

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'color', 'slug'),
                name='unique_tags',
            ),
        )

    def __str__(self):
        return self.name
