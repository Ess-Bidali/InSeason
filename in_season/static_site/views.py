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
    if request.GET.get('category'):
        print('processed')
        category = request.GET.get('category')
    if category:
        return redirect('static_site:filter', category=category)
    
    categ = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    products = paginator.get_page(page)
    filtr = category
    essentials = {'nbar': 'shop', 'categ': categ, 'products': products, 'filtr':category}
    return render(request, 'static_site/products.html', essentials )


def filter_results(request, category):
    cat = Category.objects.filter(name=category[:-1])[0]
    products = Product.objects.filter(category=cat)
        
    if request.is_ajax():
        data = serializers.serialize('json', products)
        return JsonResponse(data, safe=False)
    
    paginator = Paginator(products, 12)
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    products = paginator.get_page(page)
    categ = Category.objects.all()
    filtr = category
    essentials = {'nbar': 'shop', 'categ': categ, 'products': products, 'filtr': filtr}
    return render(request, 'static_site/products.html', essentials )