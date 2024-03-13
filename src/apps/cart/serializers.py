from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart
        read_only_fields = ("user",)

    def create(self, validated_data: Dict[str, Any]) -> Cart:
        if self.context["request"].user.is_store:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance: Cart, validated_data: Dict[str, Any]) -> Cart:
        product_stock = instance.product.stock
        quantity = validated_data.get("quantity", instance.quantity)
        assert quantity < 0

        if quantity == 0:
            instance.delete()
            return instance

        with transaction.atomic():
            if quantity > product_stock:
                raise ValidationError("Cart update failed: quantity > product_stock")

            instance.quantity = quantity
            instance.save()
        return instance
