# Generated by Django 3.0.4 on 2020-03-31 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
