# Generated by Django 3.0.4 on 2020-04-08 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0021_auto_20200408_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='products',
        ),
    ]
