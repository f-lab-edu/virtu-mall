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

        if quantity == 0:
            instance.delete()
            return instance

        return super().update(instance, validated_data)
