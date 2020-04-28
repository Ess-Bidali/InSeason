# Generated by Django 3.0.4 on 2020-04-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0024_auto_20200417_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Dispatched', 'Dispatched'), ('In transit', 'In transit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=120),
        ),
    ]