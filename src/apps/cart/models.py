from django.db import models

from apps.product.models import Product
from apps.user.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="user id",
        related_name="cart_user",
        on_delete=models.CASCADE,
        null=False,
    )
    product = models.ForeignKey(
        Product, verbose_name="product", on_delete=models.CASCADE, null=False
    )
    # PositiveSmallIntegerField: 0-32767
    quantity = models.PositiveSmallIntegerField(
        verbose_name="quantity of product", null=False
    )

    class Meta:
        db_table = "cart"
        unique_together = ("user", "product")
