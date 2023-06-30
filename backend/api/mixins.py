from rest_framework import mixins, viewsets


class CreateListRetrieveMixinsSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Сет миксинов List, Create, Retrieve."""
    pass


class ListRetrieveMixinsSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Сет миксинов List, Retrieve."""
    pass
