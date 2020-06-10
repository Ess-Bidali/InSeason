# Generated by Django 3.0.4 on 2020-05-08 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('static_site', '0040_auto_20200508_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=400, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressee', models.CharField(max_length=350)),
                ('location', models.CharField(blank=True, max_length=400, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Placed', 'Placed'), ('Dispatched', 'Dispatched'), ('In transit', 'In transit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=120)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_placed', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phone_Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('details', models.CharField(default='Small', max_length=120)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='static_site.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='static_site.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='static_site.Phone_Number'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='static_site.Customer'),
        ),
    ]
