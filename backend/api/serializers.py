from rest_framework import serializers

from recipes.models import Recipe


class MiniRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранного Recipe."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
