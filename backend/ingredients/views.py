from django_filters.rest_framework import DjangoFilterBackend

from api.filters import IngredientFilter
from api.mixins import ListRetrieveViewSet
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
