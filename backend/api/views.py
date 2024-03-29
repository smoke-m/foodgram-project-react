from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import ViewListRetrieveMixinsSet
from .permissions import AuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)
from .utils import def_favorite_shopping, shopping_cart_pdf
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, RecipeIngredients, ShoppingCart
from tags.models import Tag
from users.models import Follow, User


class TagViewSet(ViewListRetrieveMixinsSet):
    """ViewSet для таг."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ViewListRetrieveMixinsSet):
    """Вьюсет ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)


class UsersViewSet(viewsets.GenericViewSet):
    """Вьюсет пользователя."""
    @action(detail=True, url_path='subscribe', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, pk):
        """Метод создания и удаления подписки."""
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
        """Метод получения списка подписок."""
        queryset = User.objects.filter(follow__user=self.request.user).all()
        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = FollowSerializer(
            page, context={'request': request}, many=True,)
        return paginator.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецепта."""
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
        return def_favorite_shopping(
            request, get_object_or_404(Recipe, id=pk), Favorite.objects,
        )

    @action(detail=True, url_path='shopping_cart', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Метод управления корзиной."""
        return def_favorite_shopping(
            request, get_object_or_404(Recipe, id=pk), ShoppingCart.objects,
        )

    @action(detail=False, url_path='download_shopping_cart', methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Метод загрузки списка продуктов."""
        shopping_list = RecipeIngredients.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        return shopping_cart_pdf(shopping_list)
