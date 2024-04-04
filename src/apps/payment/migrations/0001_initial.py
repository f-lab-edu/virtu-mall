# Generated by Django 4.2.7 on 2024-03-01 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "total_price",
                    models.PositiveIntegerField(verbose_name="total price"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Recieved"),
                            (2, "Preparing"),
                            (3, "Shipping"),
                            (4, "Delivered"),
                            (5, "Canceled"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "shipping_address",
                    models.CharField(max_length=255, verbose_name="user address"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        default=None, null=True, verbose_name="deleted at"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified at"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="OrderDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(verbose_name="product quantity"),
                ),
                (
                    "unit_price",
                    models.PositiveIntegerField(verbose_name="product price"),
                ),
                (
                    "total_price",
                    models.PositiveIntegerField(verbose_name="total price"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        default=None, null=True, verbose_name="deleted at"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified at"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_detail",
                        to="payment.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="product.product",
                        verbose_name="product id",
                    ),
                ),
            ],
            options={
                "db_table": "order_detail",
            },
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_type",
                    models.IntegerField(
                        choices=[(0, "Deposit"), (1, "Withdrawal")], default=0
                    ),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(default=0, verbose_name="amount"),
                ),
                (
                    "mileage",
                    models.PositiveIntegerField(default=0, verbose_name="mileage"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        default=None, null=True, verbose_name="deleted at"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified at"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_wallet",
                        to="payment.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "wallet",
                "indexes": [
                    models.Index(
                        fields=["deleted_at"], name="wallet_deleted_8b27ad_idx"
                    )
                ],
            },
        ),
    ]