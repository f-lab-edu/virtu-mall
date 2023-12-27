from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from apps.payment.models import Order
from apps.payment.models import OrderDetail
from apps.payment.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["user", "balance", "mileage"]
        model = Wallet


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only = ("user",)

    def create(self, validated_data: Dict[str, Any]) -> Order:
        # TODO: payment logic & transaction

        if not self.context["request"].user.is_buyer:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user

        order_detail_data = validated_data.pop("order_detail")
        order = Order.objects.create(**validated_data)
        for detail_data in order_detail_data:
            OrderDetail.objects.create(order=order, **detail_data)
        return order

    def update(self, instance: Order, validated_data: Dict[str, Any]) -> Order:
        status = validated_data.get("status", instance.status)
        instance.status = status
        return instance
