from rest_framework import serializers

from apps.user.models import BuyerProfile, StoreProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "address"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }


class BaseProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, profile_model, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        return profile_model.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
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
    def create(self, validated_data):
        validated_data["user"]["is_buyer"] = True
        return super().create(BuyerProfile, validated_data)

    class Meta:
        model = BuyerProfile
        fields = ["user", "name", "phone"]


class StoreProfileSerializer(BaseProfileSerializer):
    def create(self, validated_data):
        validated_data["user"]["is_seller"] = True
        return super().create(StoreProfile, validated_data)

    def update(self, instance, validated_data):
        instance.business_number = validated_data.get(
            "business_number", instance.business_number
        )
        return super().update(instance, validated_data)

    class Meta:
        model = StoreProfile
        fields = ["user", "name", "phone", "business_number"]
