from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet

from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer
from utils.permissions import IsAdminOrOwner


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Cart]:
        return self.queryset.filter(user=self.request.user)
