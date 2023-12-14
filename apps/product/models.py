from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Category Name", null=False)
    created_at = models.DateTimeField(
        verbose_name="Category Created At", auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name="Category Modified At", auto_now=True
    )

    class Meta:
        db_table = "category"


class Product(models.Model):
    name = models.CharField(verbose_name="Product Name", null=False)
    price = models.CharField(verbose_name="Price", null=False)
    stock = models.CharField(
        verbose_name="Product Quantity For Sale", default=0, null=False
    )
    category = models.ForeignKey(Category, verbose_name="Category", null=False)
    description = models.CharField(verbose_name="Details", null=True)
    created_at = models.DateTimeField(
        verbose_name="Product Created At", auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name="Product Modified At", auto_now=True
    )

    class Meta:
        db_table = "product"
