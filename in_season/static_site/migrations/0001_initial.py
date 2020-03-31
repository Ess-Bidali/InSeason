# Generated by Django 3.0.4 on 2020-03-31 13:28

import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('variety', models.CharField(max_length=25)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('old_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6)),
                ('units', models.CharField(default='per kg', help_text='eg. per kg, per item', max_length=25)),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='static_site.Product')),
            ],
        ),
    ]
