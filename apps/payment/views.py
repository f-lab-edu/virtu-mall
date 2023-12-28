import json

from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.payment.models import Order
from apps.payment.models import OrderDetail
from apps.payment.models import Wallet
from apps.payment.serializers import OrderDetailSerializer
from apps.payment.serializers import OrderSerializer
from apps.payment.serializers import WalletSerializer
from apps.payment.services import rollback_pay
from apps.product.models import Product
from utils.permissions import IsAdminOrOwner
from utils.permissions import IsStore
from utils.viewsets import ModelWithoutDestroyViewSet
from utils.viewsets import RetrieveUpdateViewSet


class WalletViewSet(RetrieveUpdateViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Wallet]:
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(ModelWithoutDestroyViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)


class OrderDetailViewSet(ReadOnlyModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsStore]

    def get_queryset(self) -> QuerySet[OrderDetail]:
        user = self.request.user
        user_products = Product.objects.filter(user=user)
        return OrderDetail.objects.filter(product__in=user_products)


@api_view(["DELETE"])
def order_cancel_view(request: Request, order_id: int) -> Response:
    order = Order.objects.get(id=order_id)
    if not request.user == order.user:
        raise PermissionDenied

    if order.status != 1:
        raise ValidationError(f"delete order failed: order status is '{order.status}'")
    rollback_pay(request.user, order)

    return Response(status=status.HTTP_204_NO_CONTENT)
