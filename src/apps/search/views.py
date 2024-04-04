from rest_framework.generics import ListAPIView
from silk.profiling.profiler import silk_profile

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class SearchListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    @silk_profile(name="Search Products")
    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if query:
            return Product.objects.filter(name__search=query)
        else:
            return Product.objects.none()
