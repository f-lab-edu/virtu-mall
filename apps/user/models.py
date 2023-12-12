from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_buyer = models.BooleanField("is buyer", default=False)
    is_seller = models.BooleanField("is seller", default=False)
    address = models.CharField(verbose_name="Address", max_length=255, null=False)
    email = models.EmailField(verbose_name="Email", null=False)
    created_at = models.DateTimeField(verbose_name="User Created At", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="User Modified At", auto_now=True)

    class Meta:
        db_table = "user"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Buyer Name", max_length=20, null=False)
    phone = models.CharField(
        verbose_name="Buyer Phone Number", max_length=11, null=False
    )

    class Meta:
        db_table = "buyer"


class StoreProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Store Name", max_length=20, null=False)
    phone = models.CharField(
        verbose_name="Store Phone Number", max_length=11, null=True
    )
    business_number = models.CharField(
        verbose_name="Business Registration Number", max_length=10, null=True
    )

    class Meta:
        db_table = "store"
