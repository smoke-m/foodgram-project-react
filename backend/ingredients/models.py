from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    """Модель для  Ingredient."""
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
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
                name='unique_ingredient',
            ),
        )

    def __str__(self):
        return self.name
