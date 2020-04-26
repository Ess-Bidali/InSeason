from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Unit, Currency, Product, Order, OrderItem
from .helper_functions import filter_results, paginate, add_to_basket, remove_from_basket, items_in_basket, specific_items
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def index(request):
    products = Product.objects.all()[:4]
    in_basket = items_in_basket(request)
    capacity = len(in_basket)
    context = {'nbar': 'home', 'products': products, 'in_basket': in_basket, 'capacity': capacity}
    return render(request, 'static_site/index.html', context)


def shop(request, category=''):
    category = request.GET.get('category') if request.GET.get('category') else category
    #if category is provided, perform filter, else grab all products
    if category:
        cat = Category.objects.filter(name__iexact=category[:-1])[0]
        products = Product.objects.filter(category=cat)
        #if request is ajax, return filtered products as a json object
        if request.is_ajax(): return filter_results(products)            
    else:
        products = Product.objects.all()

    categ = Category.objects.all()
    in_basket = items_in_basket(request)
    capacity = len(in_basket)
    products = paginate(request, products)
    filtr = category[:-1]
    context = {'nbar': 'shop', 'categ': categ, 'products': products, 'filtr':filtr, 'in_basket': in_basket, 'capacity': capacity}
    return render(request, 'static_site/shop.html', context)


def single(request, product_name, key=""):
    product = get_object_or_404(Product,name__iexact=product_name).id
    product = Product.objects.get(id=product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    if request.method == "POST":
        if request.POST.get('key'): 
            remove_from_basket(request, product_name, request.POST.get('key'))
            add_to_basket(request, product_name)
            return redirect('static_site:basket') 
        else: add_to_basket(request, product_name)  
    in_basket = items_in_basket(request)
    capacity = len(in_basket)
    context = {'nbar': 'single', 'product': product, 'products': related_products, 'in_basket': in_basket, 'capacity': capacity, "key": key}
    return render(request, 'static_site/single_product.html', context)


def basket(request, product_name="", key=""):
    if product_name and key:
        print(request.session.items())
        remove_from_basket(request, product_name, key)
        print(request.session.items())
        return redirect('static_site:basket')
    in_basket = specific_items(request)
    capacity = len(in_basket)
    total = 0
    products = {}
    for product_name, value in in_basket.items():
        prod = Product.objects.get(name__iexact=product_name)
        products.update({prod:value})
        total += [val for val in value.values()][0] * prod.current_price
    context = {'nbar': 'basket', 'products': products, 'capacity': capacity, 'total': total}
    return render(request, 'static_site/my_basket.html', context)


def edit_product(request, product_name, key, act):
    return redirect('static_site:single_product_edit', product_name=product_name, key=key)


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username') if request.POST.get('username') else ''
        password = request.POST.get('password') if request.POST.get('password') else ''
        email = request.POST.get('email') if request.POST.get('email') else ''
        if username and password:
            user = User.objects.create_user(username, password=password)
            if email: 
                user.email = email
                user.save()
            login(request, user)
            print(get_object_or_404(User, email=email))
    return redirect('static_site:checkout')


@login_required()
def checkout(request):
    in_basket = specific_items(request)
    capacity = len(in_basket)
    total = 0
    products = {}
    for product_name, value in in_basket.items():
        prod = Product.objects.get(name__iexact=product_name)
        products.update({prod:value})
        total += [val for val in value.values()][0] * prod.current_price
    context = {'nbar': 'basket', 'products': products, 'capacity': capacity, 'total': total}
    return render(request, 'static_site/checkout.html', context)