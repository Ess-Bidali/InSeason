# Generated by Django 3.0.4 on 2020-05-04 08:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0036_auto_20200429_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_placed',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 4, 8, 33, 44, 685903, tzinfo=utc)),
        ),
    ]
