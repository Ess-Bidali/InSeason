from django.db import models
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User


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

    class Meta:
        ordering=['-id']
    
    def __str__(self):
        return self.name


class Phone_Number(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return self.number

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.user.username


ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Placed', 'Placed'),
    ('Dispatched', 'Dispatched'),
    ('In transit', 'In transit'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=120, default='Pending', choices=ORDER_STATUS_CHOICES)
    is_ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_placed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_total(self):
        pass

    def get_items(self):
        pass


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    details = models.CharField(max_length=120, default='Small')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{str(self.product)}_{self.details}_{self.quantity}'

    def get_total(self):
        pass
