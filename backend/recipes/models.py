from django.conf import settings
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User
from .validators import min_validator


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(max_length=settings.NAME_LENGTH)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(validators=min_validator())
    image = models.ImageField(upload_to='recipes/')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Модель количества ингредиентов в рецептах."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='in_recipe')
    amount = models.PositiveSmallIntegerField(validators=min_validator())

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredients_in_recipe'
            )
        ]

    def __str__(self):
        return f'В {self.recipe} есть {self.ingredient}'


class RecipeTags(models.Model):
    """Модель тегов рецептов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_in_tag'
            )
        ]

    def __str__(self):
        return f'У {self.recipe} тег {self.tag}'
