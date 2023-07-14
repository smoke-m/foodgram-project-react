from django.conf import settings
from django.contrib import admin

from .models import Recipe, RecipeIngredients


class RecipeIngredientsAdmin(admin.StackedInline):
    """Модель ингредиентов в рецепте."""
    model = RecipeIngredients
    autocomplete_fields = ('ingredient',)
    min_num = settings.MIN_NUM


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ зона рецептов."""
    list_display = ('id', 'name', 'text', 'pub_date', 'author',
                    'get_favorites', 'get_shopping_cart', 'cooking_time')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('pub_date', 'tags',)
    empty_value_display = settings.EMPTY_VALUE
    inlines = (RecipeIngredientsAdmin,)

    def get_favorites(self, obj):
        """Количество добавлений рецепта в избранное."""
        return obj.favorites.count()

    get_favorites.short_description = ('Рецепт в избранных.')

    def get_shopping_cart(self, obj):
        """Количество добавлений рецепта в корзины."""
        return obj.shopping_cart.count()

    get_shopping_cart.short_description = ('Рецепт в корзинах.')
