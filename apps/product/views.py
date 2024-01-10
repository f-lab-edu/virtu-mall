from datetime import datetime

from django.db.models.query import QuerySet
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from utils.permissions import IsOwnerOrReadOnly


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser,)

    def get_queryset(self) -> QuerySet[Product]:
        return self.queryset.filter(user=self.request.user, deleted_at=None)

    def perform_destroy(self, instance: Product) -> None:
        setattr(instance, "deleted_at", datetime.utcnow())
        instance.save()
