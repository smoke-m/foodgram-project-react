from django.conf import settings
from django.db import models

from api.validators import min_validator, validate_name
from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        validators=(validate_name,),
        verbose_name='Название рецепта',
        help_text='Ведите название рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Ведите описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=min_validator(),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фотография рецепта',
        help_text='Выберите фотографию рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выберите Теги',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Модель количества ингредиентов в рецептах."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент',
        help_text='Выберите из списка',
    )
    amount = models.PositiveSmallIntegerField(
        validators=min_validator(),
        verbose_name='Количество',
        help_text='Укажите количество',
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецете'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='уникальность_ингредиента_в_рецепте'
            )
        ]

    def __str__(self):
        return f'В {self.recipe} есть {self.ingredient}'


class BaseModelFavoriteShoppingCart(models.Model):
    """Базовая модель для: избранного и корзины."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.recipe} {self.user}'


class Favorite(BaseModelFavoriteShoppingCart):
    """Модель избранного."""
    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='уникальность_рецепта_в_избранном'
            )
        ]


class ShoppingCart(BaseModelFavoriteShoppingCart):
    """Модель корзины."""
    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='уникальность_рецепта_в_корзине'
            )
        ]
