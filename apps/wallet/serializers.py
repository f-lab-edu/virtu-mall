from rest_framework import serializers

from apps.wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Wallet
        read_only_fields = ("user",)
