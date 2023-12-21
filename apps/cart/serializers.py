from typing import Any
from typing import Dict

from django.core.exceptions import PermissionDenied
from django.db import models
from rest_framework import serializers

from apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart
        read_only_fields = ("user",)

    def create(self, validated_data: Dict[str, Any]) -> Any:
        if self.context["request"].user.is_store:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user.buyerprofile
        return super().create(validated_data)

    def update(self, instance: models.Model, validated_data: Dict[str, Any]) -> Any:
        # db에서 에러나니까 미리 할 필요 없을까??
        # quantity = validated_data.get("quantity")
        # if quantity < 0:
        #     raise ValueError("주문 수량은 1개 이상으로 설정해주세요.")
        quantity = validated_data.get("quantity", instance.quantity)
        if quantity > 0:
            instance.quantity = quantity
            instance.save()
        # update 함수에서 delete하는 것을 허용해줘도 될까?
        if quantity == 0:
            instance.delete()
