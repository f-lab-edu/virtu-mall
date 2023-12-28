from django.db import models

from apps.product.models import Product
from apps.user.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField(verbose_name="balance", default=0, null=False)
    mileage = models.PositiveIntegerField(verbose_name="mileage", default=0, null=False)
    last_transaction_ts = models.DateTimeField(
        verbose_name="last payment timestamp", null=True
    )
    last_transaction_amount = models.IntegerField(
        verbose_name="last payment price", null=True
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "wallet"


class Order(models.Model):
    class Status(models.IntegerChoices):
        RECIEVED = 1
        PREPARING = 2
        SHIPPING = 3
        DELIVERED = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name="total price", null=False)
    status = models.IntegerField(choices=Status.choices, default=1, null=False)
    shipping_address = models.CharField(
        verbose_name="user address", max_length=255, null=False
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "order"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, related_name="order_detail"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="product id", null=False
    )
    quantity = models.PositiveIntegerField(verbose_name="product quantity", null=False)
    unit_price = models.PositiveIntegerField(verbose_name="product price", null=False)
    total_price = models.PositiveIntegerField(verbose_name="total price", null=False)
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "order_detail"
