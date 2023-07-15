from django.conf import settings
from django.db import models

from api.validators import validate_name


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        validators=(validate_name,),
        unique=True,
        verbose_name='Имя ингредиента',
        help_text='Укажите имя ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=settings.MEASURE_LENGTH,
        verbose_name='Единицы измерения',
        help_text='Укажите единицы измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='уникальность_ингредиента_измерение.',
            ),
        )

    def __str__(self):
        return self.name
