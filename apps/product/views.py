from rest_framework.viewsets import ModelViewSet

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from utils.permissions import IsOwnerOrReadOnly


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
