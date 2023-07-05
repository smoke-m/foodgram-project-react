from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def shopping_cart_pdf(shopping_list):
    """Создание pdf файла."""
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
