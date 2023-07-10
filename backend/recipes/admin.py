from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'pub_date', 'author',
                    'get_favorites', 'get_shopping_cart')
    search_fields = ('name', 'author', 'tags')

    def get_favorites(self, obj):
        """Количество добавлений рецепта в избранное."""
        return obj.favorites.count()

    get_favorites.short_description = ('Рецепт в избранных.')

    def get_shopping_cart(self, obj):
        """Количество добавлений рецепта в корзины."""
        return obj.shopping_cart.count()

    get_shopping_cart.short_description = ('Рецепт в корзинах.')
