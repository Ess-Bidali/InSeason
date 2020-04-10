from django.contrib import admin
from .models import Category, Unit, Currency, Product, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)