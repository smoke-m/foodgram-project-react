from django_filters import rest_framework

from ingredients.models import Ingredient
from recipes.models import Recipe


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр по названию ингредиента."""
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    """
    Фильтры для выдачи рецептов: по тегам, по наличию в избранном,
    по наличию в корзине.
    """
    is_favorited = rest_framework.BooleanFilter(
        method='get_is_favorited',
        label='favorites')
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='tags')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart',
        label='shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset.exclude(favorites__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset.exclude(shopping_cart__user=self.request.user)
