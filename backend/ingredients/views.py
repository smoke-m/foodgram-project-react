from rest_framework import filters

from api.mixins import ListRetrieveMixinsSet
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(ListRetrieveMixinsSet):
    """Вьюсет модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
