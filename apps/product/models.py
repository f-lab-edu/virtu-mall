from django.db import models

from apps.user.models import StoreProfile


class Category(models.Model):
    name = models.CharField(verbose_name="Category Name", max_length=20, null=False)
    created_at = models.DateTimeField(
        verbose_name="Category Created At", auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name="Category Modified At", auto_now=True
    )

    class Meta:
        db_table = "category"


class Product(models.Model):
    name = models.CharField(verbose_name="Product Name", max_length=50, null=False)
    price = models.IntegerField(verbose_name="Price(₩)", null=False)
    stock = models.IntegerField(verbose_name="Product Quantity", default=0, null=False)
    store = models.ForeignKey(
        StoreProfile,
        verbose_name="Product Owner",
        related_name="store",
        to_field="user_id",
        on_delete=models.CASCADE,
        null=False,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        related_name="category",
        on_delete=models.CASCADE,
        null=False,
    )
    description = models.TextField(verbose_name="Details", null=True)
    created_at = models.DateTimeField(
        verbose_name="Product Created At", auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name="Product Modified At", auto_now=True
    )

    class Meta:
        db_table = "product"
