from rest_framework import mixins, viewsets


class ViewListRetrieveMixinsSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Сет миксинов просмотра."""
    pass
