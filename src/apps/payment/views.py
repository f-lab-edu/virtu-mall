from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.payment.models.order import Order
from apps.payment.models.order import OrderDetail
from apps.payment.models.wallet import Wallet
from apps.payment.serializers import OrderDetailSerializer
from apps.payment.serializers import OrderSerializer
from apps.payment.serializers import WalletSerializer
from apps.payment.services import pay_service
from apps.product.models import Product
from utils.permissions import IsAdminOrOwner
from utils.permissions import IsStore
from utils.viewsets import CreateViewSet


class WalletViewSet(CreateViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAdminOrOwner]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user, deleted_at=None).order_by(
            "-created_at"
        )

    def perform_destroy(self, instance: Order) -> None:
        if not self.request.user == instance.user:
            raise PermissionDenied

        if instance.status != instance.Status.RECIEVED:
            raise ValidationError(
                f"delete order failed: order status is '{instance.status}'"
            )

        pay_service.rollback_pay(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetailViewSet(ReadOnlyModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsStore]

    def get_queryset(self) -> QuerySet[OrderDetail]:
        user = self.request.user
        user_products = Product.objects.filter(user=user)
        return OrderDetail.objects.filter(product__in=user_products).order_by(
            "-created_at"
        )
