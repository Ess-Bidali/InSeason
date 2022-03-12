# Generated by Django 3.0.4 on 2020-05-08 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('static_site', '0041_auto_20200508_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='static_site.Unit'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='stock',
            name='product',
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_stock', to='static_site.Product'),
        ),
    ]