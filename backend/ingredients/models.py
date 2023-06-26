from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=settings.NAME_LENGTH)
    measurement_unit = models.CharField(max_length=settings.MEASURE_LENGTH)

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name
