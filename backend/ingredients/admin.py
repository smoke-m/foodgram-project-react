from django.conf import settings
from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ зона ингредиента."""
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = settings.EMPTY_VALUE
