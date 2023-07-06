from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredients
from tags.models import Tag
from users.models import User
from .validators import min_validator


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class MiniRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранного Recipe."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class PasswordChangeSerializer(SetPasswordSerializer):
    """Сериализатор смены пароля."""
    current_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True,)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Не верный пароль.')
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'Новый пароль должен содержать не мене 8-ми символов.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',
                  'is_subscribed']
        read_only_fields = ['id', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.follow.exists()


class CreteUserSerializer(UserCreateSerializer):
    """Сериализатор регистрации модели User."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'email',
                  'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class FollowSerializer(UserSerializer):
    """Сериализатор получения подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except ValueError:
                pass
        return MiniRecipeSerializer(recipes, many=True).data

    def validate(self, attrs):
        if self.context['request'].user == self.instance:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return attrs


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
    image = Base64ImageField(use_url=True, required=False)

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
        recipe_ingredients = [
            RecipeIngredients(
                ingredient=get_object_or_404(Ingredient, pk=element['id']),
                recipe=recipe,
                amount=element['amount']
            )
            for element in ingredients
        ]
        RecipeIngredients.objects.bulk_create(recipe_ingredients)

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
