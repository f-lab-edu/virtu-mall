from django.db import models

from apps.user.models import User


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    deleted_at = models.DateTimeField(
        verbose_name="deleted at",
        default=None,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "wallet"
        indexes = [models.Index(fields=["deleted_at"])]

    @classmethod
    def get_balance(cls, user: User) -> int:
        return cls.objects.get(user=user, deleted_at=None).amount
