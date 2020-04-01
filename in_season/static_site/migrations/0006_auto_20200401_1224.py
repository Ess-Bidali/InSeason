# Generated by Django 3.0.4 on 2020-04-01 09:24

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0005_auto_20200401_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=django.core.files.storage.FileSystemStorage(location='media.static_site.products.%Y.%m/')),
        ),
    ]
