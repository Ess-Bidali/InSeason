# Generated by Django 3.0.4 on 2020-04-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0028_auto_20200426_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='location',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
