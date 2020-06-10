from django.db import models
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    market_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    image = models.ImageField(upload_to='products/%Y.%m', blank=True, null=True)
    is_available = models.BooleanField(default=False)

    class Meta:
        ordering=['-id']
    
    def __str__(self):
        return self.name

    def discount(self):
        discount = self.market_price - self.current_price
        return 0 if discount < 0 else discount

    def percentage_discount(self):
        return round(self.discount()/self.current_price * 100)


class Variety(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variety")

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name="in_stock")
    variety = models.ForeignKey(Variety, on_delete=models.SET_NULL, blank=True, null=True)
    details = models.CharField(max_length=120, default='Small')
    quantity = models.IntegerField(default=0)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product','variety','details']

    def __str__(self):
        return f'{self.product}_{self.details}'

    def save(self, *args, **kwargs):
        if self.quantity > 0 and self.product.is_available == False: 
            self.product.is_available = True
            self.product.save()
        super().save(*args, **kwargs)


class Phone_Number(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="phone_number")
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=400, blank=True, null=True)

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
    addressee = models.CharField(max_length=350)
    contact = models.ForeignKey(Phone_Number, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=120, default='Pending', choices=ORDER_STATUS_CHOICES)
    is_ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_placed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer}_{self.status}'


    def get_order_items(self):
        return self.products.all()
    
    def get_total(self, total=0, deal=0):
        items = {}
        products = self.get_order_items()
        for order_item in products:
            product_total = order_item.get_total()
            product = order_item.product
            if order_item.product in items.keys():
                items[product].update({order_item:order_item.quantity})
            else:
                items.update({product: {order_item:order_item.quantity}})
            total += product_total
            if product.discount(): deal += product.discount()
        return items, total, deal


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    details = models.CharField(max_length=120, default='Small')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{str(self.product).lower()}_{self.details}'

    def get_total(self):
        return self.product.current_price * self.quantity

    def check_for_deal(self):
        return 0 if self.product.discount < 0 else self.product.discount
