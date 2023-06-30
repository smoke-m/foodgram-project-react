from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import MiniRecipeSerializer
from api.permissions import AuthorOrAdminOrReadOnly
from .models import Favorite, Recipe, RecipeIngredients, ShoppingCart
from .serializers import CreateRecipeSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        """Выбор сериализатора. """
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        elif self.action in ('create', 'partial_update'):
            return CreateRecipeSerializer

    def get_serializer_context(self):
        """Передача контекста. """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(detail=True, url_path='favorite', methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        """Метод управления избранным."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
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
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепта нет в корзине'},
                        status=status.HTTP_400_BAD_REQUEST)

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
        shopping_list_text = 'Список покупок:\n\n'
        for ingredient in shopping_list:
            shopping_list_text += (
                f"{ingredient['ingredient__name']}  - {ingredient['sum']}"
                f"({ingredient['ingredient__measurement_unit']})\n")
        return HttpResponse(shopping_list_text, content_type="text/plain")
