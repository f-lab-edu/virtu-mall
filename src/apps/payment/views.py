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

    def create(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        if not user.is_buyer:
            raise PermissionDenied

        order_detail_data = request.data.get("order_detail", [])
        total_price = self._calculate_total_price(order_detail_data)

        self._prepare_request_data(request, user, total_price)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pay_service.pay(request.data, order_detail_data)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_destroy(self, instance: Order) -> Response:
        if not self.request.user == instance.user:
            raise PermissionDenied

        if instance.status != instance.Status.RECIEVED:
            raise ValidationError(
                f"delete order failed: order status is '{instance.status}'"
            )

        pay_service.rollback_pay(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _calculate_total_price(self, order_detail_data: dict[str, any]) -> int:
        return sum([item.get("total_price", 0) for item in order_detail_data])

    def _prepare_request_data(self, request, user, total_price):
        request.data.update(
            {
                "user": user.id,
                "total_price": total_price,
                "shipping_address": user.address,
            }
        )


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
