# Generated by Django 3.0.4 on 2020-04-21 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0026_auto_20200421_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_placed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
