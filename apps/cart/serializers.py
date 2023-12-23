from typing import Any, Dict

from django.core.exceptions import PermissionDenied
from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart
        read_only_fields = ("user",)

    def create(self, validated_data: Dict[str, Any]) -> Any:
        if self.context["request"].user.is_store:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance: models.Model, validated_data: Dict[str, Any]) -> Any:
        product_stock = instance.product.stock
        quantity = validated_data.get("quantity", instance.quantity)
        if quantity > product_stock:
            raise ValidationError(f"재고가 충분하지 않습니다. 주문 수량을 {product_stock}개 이하로 지정해주세요.")

        # db에서 에러나니까 미리 할 필요 없을까??
        # if quantity < 0:
        #     raise ValidationError("주문 수량은 1개 이상으로 설정해주세요.")

        if quantity > 0:
            instance.quantity = quantity
            instance.save()

        # update 함수에서 delete하는 것을 허용해줘도 될까?
        if quantity == 0:
            instance.delete()
        return instance
