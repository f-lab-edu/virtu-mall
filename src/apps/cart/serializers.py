from typing import Any
from typing import Dict

from rest_framework import serializers

from apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart
        read_only_fields = ("user",)

    def create(self, validated_data: dict[str, Any]) -> Cart:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance: Cart, validated_data: Dict[str, Any]) -> Cart:
        validated_data["user"] = self.context["request"].user
        quantity = validated_data.get("quantity", instance.quantity)
        override = validated_data.get("override", False)

        assert quantity >= 0

        if quantity == 0:
            instance.delete()
            return instance

        if not override:
            validated_data["quantity"] += instance.quantity
        return super().update(instance, validated_data)
