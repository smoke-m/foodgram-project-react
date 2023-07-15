from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from .serializers import MiniRecipeSerializer


def shopping_cart_pdf(shopping_list):
    """Создание пдф файла."""
    buffer = BytesIO()
    font_path = ('fonts/arial.ttf')
    pdfmetrics.registerFont(TTFont('Arial', font_path))
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont('Arial', 20)
    y = 700
    for ingredient in shopping_list:
        text = (
            f"{ingredient['ingredient__name']}  - {ingredient['sum']}"
            f"({ingredient['ingredient__measurement_unit']})")
        pdf.drawString(100, y, text)
        y -= 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopping.pdf"'
    response.write(buffer.getvalue())
    return response


def def_favorite_shopping(request, recipe, model):
    """Функция логики избраного и корзины."""
    if request.method == 'POST':
        if model.filter(user=request.user, recipe=recipe).exists():
            return Response({'errors': 'Рецепт уже добавлен'},
                            status=status.HTTP_400_BAD_REQUEST)
        model.create(user=request.user, recipe=recipe).save()
        serializer = MiniRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    model.filter(user=request.user, recipe=recipe).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
