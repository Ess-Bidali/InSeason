# Generated by Django 3.0.4 on 2020-05-08 15:56

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0043_auto_20200508_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='amount_available',
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6),
        ),
    ]
