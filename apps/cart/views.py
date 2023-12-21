from rest_framework.viewsets import ModelViewSet

from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer
from utils.permissions import IsAdminOrOwner


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminOrOwner]
