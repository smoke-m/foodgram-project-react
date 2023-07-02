from api.mixins import ListRetrieveViewSet
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
