# Generated by Django 3.0.4 on 2020-04-01 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0015_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='units',
            new_name='unit',
        ),
    ]
