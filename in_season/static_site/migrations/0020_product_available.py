# Generated by Django 3.0.4 on 2020-04-08 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0019_remove_product_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
