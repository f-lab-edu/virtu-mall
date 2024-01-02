from django.db import models
from model_utils.models import TimeStampedModel

from apps.product.models import Product
from apps.user.models import User


class Wallet(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.PositiveIntegerField(verbose_name="balance", default=0, null=False)
    mileage = models.PositiveIntegerField(verbose_name="mileage", default=0, null=False)

    class Meta:
        db_table = "wallet"


class Order(TimeStampedModel):
    class Status(models.IntegerChoices):
        RECIEVED = 1
        PREPARING = 2
        SHIPPING = 3
        DELIVERED = 4
        CANCELED = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name="total price", null=False)
    status = models.IntegerField(choices=Status.choices, default=1, null=False)
    shipping_address = models.CharField(
        verbose_name="user address", max_length=255, null=False
    )

    class Meta:
        db_table = "order"


class OrderDetail(TimeStampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, related_name="order_detail"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="product id", null=False
    )
    quantity = models.PositiveIntegerField(verbose_name="product quantity", null=False)
    unit_price = models.PositiveIntegerField(verbose_name="product price", null=False)
    total_price = models.PositiveIntegerField(verbose_name="total price", null=False)

    class Meta:
        db_table = "order_detail"
