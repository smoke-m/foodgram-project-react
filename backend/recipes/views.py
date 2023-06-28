from rest_framework import viewsets

from .models import Recipe
from .permissions import AuthorOrAdminOrReadOnly
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
