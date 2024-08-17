from typing import Any
from typing import Dict

from rest_framework import serializers

from apps.payment.models.order import Order
from apps.payment.models.order import OrderDetail
from apps.payment.models.wallet import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["user", "transaction_type", "amount", "mileage"]
        model = Wallet


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ["user", "total_price", "shipping_address", "order_detail"]

    def create(self, validated_data: Dict[str, Any]) -> Order:
        order_detail_data = validated_data.pop("order_detail")
        order = Order.objects.create(**validated_data)

        OrderDetail.objects.bulk_create(
            [
                OrderDetail(order=order, **detail_data)
                for detail_data in order_detail_data
            ]
        )
        return order

    def update(self, instance: Order, validated_data: dict[str, Any]) -> Order:
        instance.status = validated_data.get("status", instance.status)
        return super().update(instance, validated_data)
