from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from model_utils.models import TimeStampedModel

from apps.payment.models.order import Order
from apps.user.models import User


class Wallet(TimeStampedModel):
    class TransactionType(models.IntegerChoices):
        DEPOSIT = 0
        WITHDRAWAL = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.IntegerField(
        choices=TransactionType.choices,
        default=TransactionType.DEPOSIT,
        null=False,
    )
    amount = models.PositiveIntegerField(
        verbose_name="amount",
        default=0,
        null=False,
    )
    mileage = models.PositiveIntegerField(
        verbose_name="mileage",
        default=0,
        null=False,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        related_name="order_wallet",
    )
    deleted = models.DateTimeField(
        verbose_name="deleted at",
        default=None,
        null=True,
    )

    class Meta:
        db_table = "wallet"

    @classmethod
    def get_balance(cls, user: User) -> int:
        deposits = cls.objects.filter(
            user=user,
            transaction_type=Wallet.TransactionType.DEPOSIT,
            deleted=None,
        ).aggregate(amount=Coalesce(Sum("amount"), 0))["amount"]

        withdrawals = cls.objects.filter(
            user=user,
            transaction_type=Wallet.TransactionType.WITHDRAWAL,
            deleted=None,
        ).aggregate(amount=Coalesce(Sum("amount"), 0))["amount"]
        return deposits - withdrawals
