from django.db import models
from decimal import Decimal
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=25)
    variety = models.CharField(max_length=25, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/%Y.%m', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)