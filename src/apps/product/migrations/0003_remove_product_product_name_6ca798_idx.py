# Generated by Django 4.2.7 on 2024-04-04 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0002_alter_product_options_alter_product_unique_together_and_more",
        ),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="product",
            name="product_name_6ca798_idx",
        ),
    ]
