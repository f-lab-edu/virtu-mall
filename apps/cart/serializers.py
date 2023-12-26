from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db import models
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

    def update(self, instance: models.Model, validated_data: Dict[str, Any]) -> Cart:
        product_stock = instance.product.stock
        quantity = validated_data.get("quantity", instance.quantity)
        assert quantity < 0

        if quantity == 0:
            instance.delete()
            return instance

        with transaction.atomic():
            if quantity > product_stock:
                raise ValidationError("재고 부족으로 주문 불가")

            instance.quantity = quantity
            instance.save()
        return instance
