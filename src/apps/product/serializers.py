from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from rest_framework import serializers

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
        validated_data["deleted_at"] = None
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
