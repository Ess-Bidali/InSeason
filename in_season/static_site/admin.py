from django.contrib import admin
from .models import Category, Unit, Currency, Product, Variety, Stock, Phone_Number, Customer, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Currency)
admin.site.register(Product)
admin.site.register(Variety)
admin.site.register(Stock)
admin.site.register(Phone_Number)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)