from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.payment.models import Order
from apps.payment.models import OrderDetail
from apps.payment.models import Wallet
from apps.payment.serializers import OrderDetailSerializer
from apps.payment.serializers import OrderSerializer
from apps.payment.serializers import WalletSerializer
from apps.product.models import Product
from utils.permissions import IsAdminOrOwner
from utils.permissions import IsStore
from utils.viewsets import RetrieveUpdateViewSet


class WalletViewSet(RetrieveUpdateViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Wallet]:
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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
