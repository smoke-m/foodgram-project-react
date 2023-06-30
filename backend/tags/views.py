from api.mixins import ListRetrieveMixinsSet
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ListRetrieveMixinsSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
