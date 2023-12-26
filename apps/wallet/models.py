from django.db import models

from apps.user.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(verbose_name="balance", default=0, null=False)
    mileage = models.IntegerField(verbose_name="mileage", default=0, null=False)
    last_transaction_ts = models.DateTimeField(
        verbose_name="last payment timestamp", null=True
    )
    last_transaction_amount = models.IntegerField(
        verbose_name="last payment price", null=True
    )
    created_at = models.DateTimeField(
        verbose_name="wallet created at", auto_now_add=True
    )
    modified_at = models.DateTimeField(verbose_name="wallet modified at", auto_now=True)

    class Meta:
        db_table = "wallet"
