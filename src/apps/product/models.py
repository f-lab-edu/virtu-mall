from django.db import models

from apps.user.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name="category Name",
        max_length=20,
        null=False,
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "category"


def product_image_path(instance, filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/
    return f"store/{instance.user}/product/{instance.name}/{filename}"


class Product(models.Model):
    name = models.CharField(
        verbose_name="product name",
        max_length=50,
        null=False,
    )
    price = models.IntegerField(
        verbose_name="price(₩)",
        null=False,
    )
    stock = models.PositiveIntegerField(
        verbose_name="product quantity",
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
        verbose_name="product owner",
        related_name="store",
        on_delete=models.CASCADE,
        null=False,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="category",
        related_name="category",
        on_delete=models.PROTECT,
        null=False,
    )
    description = models.TextField(verbose_name="details", null=True)
    deleted_at = models.DateTimeField(
        verbose_name="product deleted at", default=None, null=True
    )
    created_at = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="modified at", auto_now=True)

    class Meta:
        db_table = "product"
        unique_together = ("name", "user")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-name"]),
        ]
