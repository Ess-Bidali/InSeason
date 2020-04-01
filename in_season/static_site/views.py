from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, 'static_site/index.html', {'nbar': 'home'})

def shop(request):
    categ = Category.objects.all()
    products = Product.objects.all()
    essentials = {'nbar': 'shop', 'categ': categ, 'products': products}
    return render(request, 'static_site/shop.html', essentials )