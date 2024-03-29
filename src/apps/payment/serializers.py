from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from apps.payment.models.order import Order
from apps.payment.models.order import OrderDetail
from apps.payment.models.wallet import Wallet
from apps.payment.services import pay


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
        read_only_fields = ("user", "total_price", "shipping_address")

    def create_order_details(
        self, order: Order, order_detail_data: dict[str, Any]
    ) -> None:
        OrderDetail.objects.bulk_create(
            [
                OrderDetail(order=order, **detail_data)
                for detail_data in order_detail_data
            ]
        )

    def create(self, validated_data: Dict[str, Any]) -> Order:
        user = self.context["request"].user
        if not user.is_buyer:
            raise PermissionDenied

        validated_data["user"] = user
        validated_data["shipping_address"] = user.address
        order_detail_data = validated_data.pop("order_detail")
        validated_data["total_price"] = sum(
            [order_detail["total_price"] for order_detail in order_detail_data]
        )
        wallet = pay(validated_data, order_detail_data)

        order = super().create(validated_data)
        self.create_order_details(order, order_detail_data)
        wallet.order = order
        wallet.save()
        return order

    def update(self, instance: Order, validated_data: dict[str, Any]) -> Order:
        instance.status = validated_data.get("status", instance.status)
        return super().update(instance, validated_data)
