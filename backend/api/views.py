from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredients
from tags.models import Tag
from users.models import Follow, User
from .filters import IngredientFilter, RecipeFilter
from .mixins import ListRetrieveMixinsViewSet
from .permissions import AuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FollowSerializer,
                          IngredientSerializer, MiniRecipeSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer)
from .utils import shopping_cart_pdf


class TagViewSet(ListRetrieveMixinsViewSet):
    """ViewSet для Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_paginated_response(self, data):
        return Response(data)


class IngredientViewSet(ListRetrieveMixinsViewSet):
    """Вьюсет модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)

    def get_paginated_response(self, data):
        return Response(data)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, url_path='subscribe', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, pk):
        """Метод создания и удаления 'subscribe'."""
        author = get_object_or_404(User, id=pk)
        try:
            if request.method == 'POST':
                Follow.objects.create(user=request.user, author=author).save()
                serializer = FollowSerializer(
                    author, context={'request': request},)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            Follow.objects.filter(user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as error:
            return Response({'errors': f'{error}'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='subscriptions', methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        """Метод получения списка 'subscriptions'."""
        queryset = User.objects.filter(follow__user=self.request.user).all()
        if queryset:
            queryset_pag = self.paginate_queryset(queryset)
            serializer = FollowSerializer(
                queryset_pag, context={'request': request}, many=True,)
            return self.get_paginated_response(serializer.data)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Выбор сериализатора. """
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update'):
            return CreateRecipeSerializer

    @action(detail=True, url_path='favorite', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        """Метод управления избранным."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if recipe.favorited_by.filter(id=user.id).exists():
                return Response({'errors': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.favorited_by.add(user)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if recipe.favorited_by.filter(id=user.id).exists():
            recipe.favorited_by.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в избраном'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path='shopping_cart', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Метод управления корзиной."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if recipe.shopping_cart.filter(id=user.id).exists():
                return Response({'errors': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe.shopping_cart.add(user)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if recipe.shopping_cart.filter(id=user.id).exists():
            recipe.shopping_cart.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в корзине'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='download_shopping_cart', methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Метод загрузки списка продуктов."""
        shopping_list = RecipeIngredients.objects.filter(
            recipe__in=request.user.shopping.all()
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        return shopping_cart_pdf(shopping_list)
