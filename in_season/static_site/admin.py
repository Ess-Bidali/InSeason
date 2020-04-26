from django.contrib import admin
from .models import Category, Unit, Currency, Product, Phone_Number, Customer, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Product)
admin.site.register(Phone_Number)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order)