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

    def perform_destroy(self, instance: QuerySet) -> None:
        setattr(instance, "deleted_at", datetime.utcnow())
        instance.save()
