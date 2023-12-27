from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.payment.models import Order
from apps.payment.models import Wallet
from apps.payment.serializers import OrderSerializer
from apps.payment.serializers import WalletSerializer
from utils.permissions import IsAdminOrOwner
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
    # TODO: create 할 때는 권한 확인 안하도록...
    # permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Order]:
        return self.queryset.filter(user=self.request.user)
