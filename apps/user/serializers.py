from rest_framework import serializers

from apps.user.models import BuyerProfile, StoreProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "address"]


class BaseProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create_user_profile(self, profile_model, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        return profile_model.objects.create(user=user, **validated_data)


# TODO: update
class BuyerProfileSerializer(BaseProfileSerializer):
    def create(self, validated_data):
        validated_data["user"]["is_buyer"] = True
        return self.create_user_profile(BuyerProfile, validated_data)

    class Meta:
        model = BuyerProfile
        fields = ["user", "name", "phone"]


# TODO: update
class StoreProfileSerializer(BaseProfileSerializer):
    def create(self, validated_data):
        validated_data["user"]["is_seller"] = True
        return self.create_user_profile(StoreProfile, validated_data)

    class Meta:
        model = StoreProfile
        fields = ["user", "name", "phone"]
