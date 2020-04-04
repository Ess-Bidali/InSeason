from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    products = Product.objects.all()[:4]
    essentials = {'nbar': 'home', 'products': products}
    return render(request, 'static_site/index.html', essentials)


def shop(request, category=''):
    category = request.GET.get('category') if request.GET.get('category') else category
    #if category is provided, perform filter, else grab all products
    if category:
        cat = Category.objects.filter(name=category[:-1])[0]
        products = Product.objects.filter(category=cat)
        #if request is ajax, return filtered products as a json object
        if request.is_ajax(): return filter_results(products)            
    else:
        products = Product.objects.all()

    categ = Category.objects.all()
    products = paginate(request, products)
    filtr = category[:-1]
    essentials = {'nbar': 'shop', 'categ': categ, 'products': products, 'filtr':filtr}
    return render(request, 'static_site/products.html', essentials )


def filter_results(products):
    data = serializers.serialize('json', products)
    return JsonResponse(data, safe=False)

def paginate(request, products):
    #initialize Paginator object with products and limit of items per page as parameters
    paginator = Paginator(products, 12) 
    #get requested page number, else get page 1
    page = request.GET.get('page') if request.GET.get('page') else 1
    return paginator.get_page(page)

def single(request):
    essentials = {'nbar': 'single'}
    return render(request, 'static_site/single_product.html', essentials)