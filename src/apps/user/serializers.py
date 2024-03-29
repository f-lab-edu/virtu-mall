from typing import Any
from typing import Dict
from typing import Type

from django.db import models
from rest_framework import serializers

from apps.user.models import BuyerProfile
from apps.user.models import StoreProfile
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "address"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }


class BaseProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create_user_model(
        self,
        profile_model: Type[models.Model],
        validated_data: Dict[str, Any],
        user_field: str,
    ) -> models.Model:
        validated_data["user"][user_field] = True
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        return profile_model.objects.create(user=user, **validated_data)

    def update(
        self, instance: models.Model, validated_data: Dict[str, Any]
    ) -> models.Model:
        instance.name = validated_data.get("name", instance.name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        user_data = validated_data.get("user")
        user = instance.user

        if user_data:
            user.username = user_data.get("username", user.username)
            user.email = user_data.get("email", user.email)
            user.address = user_data.get("address", user.address)
            user.save()
        return instance


class BuyerProfileSerializer(BaseProfileSerializer):
    def create(self, validated_data: Dict[str, Any]) -> BuyerProfile:
        return self.create_user_model(BuyerProfile, validated_data, "is_buyer")

    class Meta:
        model = BuyerProfile
        fields = ["user", "name", "phone"]


class StoreProfileSerializer(BaseProfileSerializer):
    def create(self, validated_data: Dict[str, Any]) -> StoreProfile:
        return self.create_user_model(StoreProfile, validated_data, "is_store")

    def update(
        self, instance: StoreProfile, validated_data: Dict[str, Any]
    ) -> StoreProfile:
        instance.business_number = validated_data.get(
            "business_number", instance.business_number
        )
        return super().update(instance, validated_data)

    class Meta:
        model = StoreProfile
        fields = ["user", "name", "phone", "business_number"]
