import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers

from api.validators import min_validator
from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer
from .models import Recipe, RecipeIngredients


class Base64ImageField(serializers.ImageField):
    """Поле кодирования изображения в base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateRecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в создании рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(validators=min_validator())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор получения рецептов."""
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = RecipeIngredientsSerializer(
        source='ingredient_list', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorited_by.filter(id=user.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(id=user.id).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов."""
    ingredients = CreateRecipeIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name',
                  'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        """Представление модели."""
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def validate_ingredients(self, data):
        """Валидация ингредиентов"""
        ingredients = self.initial_data.get('ingredients')
        lst_ingredient = []
        for ingredient in ingredients:
            if ingredient['id'] in lst_ingredient:
                raise exceptions.ValidationError('Ингредиенты уникальны!.')
            lst_ingredient.append(ingredient['id'])
        return data

    def create_ingredients(self, ingredients, recipe):
        """Создание ингредиента."""
        for element in ingredients:
            ingredient = get_object_or_404(Ingredient, pk=element['id'])
            RecipeIngredients.objects.create(
                ingredient=ingredient, recipe=recipe, amount=element['amount']
            )

    def create(self, validated_data):
        """Создания модели Recipe."""
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Обновление модели Recipe."""
        RecipeIngredients.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)
