from rest_framework.generics import ListAPIView

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class SearchListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if query:
            return Product.objects.filter(name__icontains=query)
        else:
            return Product.objects.none()
