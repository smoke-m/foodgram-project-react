from io import BytesIO
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.serializers import MiniRecipeSerializer
from api.permissions import AuthorOrAdminOrReadOnly
from .models import Recipe, RecipeIngredients
from .serializers import CreateRecipeSerializer, RecipeSerializer


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
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        y = 700
        for ingredient in shopping_list:
            text = (
                f"{ingredient['ingredient__name']}  - {ingredient['sum']}"
                f"({ingredient['ingredient__measurement_unit']})\n")
            pdf.drawString(100, y, text)
            y -= 20
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping.pdf"'
        response.write(buffer.getvalue())
        return response

        # shopping_list_text = 'Список покупок:\n\n'
        # for ingredient in shopping_list:
        #     shopping_list_text += (
        #         f"{ingredient['ingredient__name']}  - {ingredient['sum']}"
        #         f"({ingredient['ingredient__measurement_unit']})\n")
        # return HttpResponse(shopping_list_text, content_type="text/plain")
