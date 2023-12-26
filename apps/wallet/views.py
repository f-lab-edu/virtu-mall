from django.db.models.query import QuerySet

from apps.wallet.models import Wallet
from apps.wallet.serializers import WalletSerializer
from utils.permissions import IsAdminOrOwner
from utils.viewsets import RetrieveUpdateViewSet


class WalletViewSet(RetrieveUpdateViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self) -> QuerySet[Wallet]:
        return self.queryset.filter(user=self.request.user)
