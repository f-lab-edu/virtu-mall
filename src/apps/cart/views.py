from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.cart.cart import DBCart
from apps.cart.cart import SessionCart
from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        instance = Cart.objects.get(
            user=self.request.user,
            product=self.request.data.get("product"),
        )
        return instance

    def _get_cart(self):
        if self.request.user.is_authenticated:
            return DBCart(self.request.user, self)
        else:
            return SessionCart(self.request)

    def get_queryset(self) -> QuerySet[Cart]:
        cart = self._get_cart()
        return cart.get_items()

    def add(self, request, *args, **kwargs) -> QuerySet[Cart]:
        cart = self._get_cart()
        cart.add(request, *args, **kwargs)
        return Response({"status": "product added"}, status=status.HTTP_200_OK)

    def remove(self, request, *args, **kwargs) -> QuerySet[Cart]:
        cart = self._get_cart()
        cart.remove(request, *args, **kwargs)
        return Response(
            {"status": "product removed"}, status=status.HTTP_204_NO_CONTENT
        )
