# Generated by Django 4.2.7 on 2024-04-04 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunSQL(
            ("CREATE FULLTEXT INDEX product_name_fulltext_index ON product(name)",),
            ("DROP INDEX product_name_fulltext_index ON product",),
        ),
    ]
