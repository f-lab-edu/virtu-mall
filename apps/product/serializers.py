from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from apps.payment.models.order import OrderDetail
from apps.product.models import Category
from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product
        read_only_fields = ("user",)

    def create(self, validated_data: Dict[str, Any]) -> Product:
        if self.context["request"].user.is_buyer:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation["stock"] = (
            instance.stock
            - OrderDetail.objects.filter(product=instance).aggregate(
                stock=Coalesce(Sum("quantity"), 0)
            )["stock"]
        )
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
