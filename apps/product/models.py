from django.db import models
from model_utils.models import TimeStampedModel

from apps.user.models import User


class Category(TimeStampedModel):
    name = models.CharField(
        verbose_name="Category Name",
        max_length=20,
        null=False,
    )

    class Meta:
        db_table = "category"


def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/
    return f"store/{instance.user}/product/{instance.name}/{filename}"


class Product(TimeStampedModel):
    name = models.CharField(
        verbose_name="Product Name",
        max_length=50,
        null=False,
    )
    price = models.IntegerField(
        verbose_name="Price(₩)",
        null=False,
    )
    stock = models.PositiveIntegerField(
        verbose_name="Product Quantity",
        default=0,
        null=False,
    )
    image = models.ImageField(
        upload_to=product_image_path,
        default=None,
        null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Product Owner",
        related_name="store",
        on_delete=models.CASCADE,
        null=False,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        related_name="category",
        on_delete=models.PROTECT,
        null=False,
    )
    description = models.TextField(verbose_name="Details", null=True)
    deleted = models.DateTimeField(
        verbose_name="Product Deleted At", default=None, null=True
    )

    class Meta:
        db_table = "product"
        unique_together = ("name", "user")