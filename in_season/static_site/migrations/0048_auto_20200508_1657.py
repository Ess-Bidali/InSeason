# Generated by Django 3.0.4 on 2020-05-08 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0047_product_is_available'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount',
            new_name='market_price',
        ),
    ]