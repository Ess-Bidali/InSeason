from django.db import models
from decimal import Decimal
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=25)
    variety = models.CharField(max_length=25)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    units = models.CharField(max_length=25, default='per kg', help_text='eg. per kg, per item')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)