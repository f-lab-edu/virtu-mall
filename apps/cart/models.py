from django.db import models

from apps.product.models import Product
from apps.user.models import BuyerProfile


class Cart(models.Model):
    user = models.ForeignKey(
        BuyerProfile,
        verbose_name="Buyer ID",
        related_name="cart_user",
        to_field="user_id",
        on_delete=models.CASCADE,
        null=False,
    )
    product = models.ForeignKey(
        Product, verbose_name="Product ID", on_delete=models.CASCADE, null=False
    )
    # PositiveSmallIntegerField: 0-32767
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Quantity of Product", null=False
    )

    class Meta:
        db_table = "cart"
        unique_together = ("user", "product")
