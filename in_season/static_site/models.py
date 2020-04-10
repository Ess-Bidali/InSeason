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


class Currency(models.Model):
    name = models.CharField(max_length=25)
    abbreviation = models.CharField(max_length=25)

    def __str__(self):
        return self.abbreviation


class Product(models.Model):
    name = models.CharField(max_length=25)
    variety = models.CharField(max_length=25, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    amount_available = models.IntegerField(null=True)
    image = models.ImageField(upload_to='products/%Y.%m', blank=True, null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    contact = models.IntegerField()
    location = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product

    def get_total(self):
        pass


ORDER_STATUS_CHOICES = (
    ('Not yet dispatched', 'Not yet dispatched'),
    ('Dispatched', 'Dispatched'),
    ('In transit', 'In transit'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    status = models.CharField(max_length=120, default='Not yet dispatched', choices=ORDER_STATUS_CHOICES)
    is_ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(OrderItem)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.id

    def get_total(self):
        pass

    def get_items(self):
        pass
