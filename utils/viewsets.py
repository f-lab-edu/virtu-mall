from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    """
    A viewset that provides default `retrieve()`, `update()`actions.
    """

    pass


class ModelWithoutDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    pass
