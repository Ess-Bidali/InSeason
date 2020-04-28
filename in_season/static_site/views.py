from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Unit, Currency, Product, Order, OrderItem, Customer
from .helper_functions import get_json_respose, paginate, add_to_basket, remove_from_basket, get_context, get_total_cost, add_order_items, remove_from_db_basket, add_to_db_basket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from decimal import *
from django.http import Http404

DEAL_OF_THE_DAY = 'avocado'
DISCOUNT = Decimal('3.00')

def index(request):
    products = Product.objects.all()[:4]
    deal = get_object_or_404(Product, name__iexact=DEAL_OF_THE_DAY)
    context = get_context(request, 'home', products)
    context.update({'deal': deal})
    return render(request, 'static_site/index.html', context)

#static pages
def static_pages(request, page):
    context = get_context(request, 'home')
    if page == 'terms-and-conditions': return render(request, 'static_site/terms.html', context)
    elif page == 'privacy-policy': return render(request, 'static_site/privacy_policy.html', context)
    elif page == 'FAQs': return render(request, 'static_site/faqs.html', context)
    else : return render(request, 'static_site/privacy_policy.html', context)


def contact(request):
    context = get_context(request, 'contact')
    return render(request, 'static_site/contact.html', context)


def shop(request, category=''):
    #if category is provided, perform filter, else grab all products
    if category:
        category = category[:-1]
        cat = Category.objects.filter(name__iexact=category)[0]
        products = cat.product_set.all() #all products under this category

        #if request is ajax, return filtered products as a json object
        if request.is_ajax(): return get_json_respose(products)            
    else:
        products = Product.objects.all()
    categs = Category.objects.all()
    products = paginate(request, products)
    filtr = category
    context = get_context(request, 'shop', products)
    context.update({'categs': categs, 'filtr':filtr})
    return render(request, 'static_site/shop.html', context)


def single(request, product_name, edit=""):
    product = get_object_or_404(Product,name__iexact=product_name).id
    product = Product.objects.get(id=product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    if request.method == "POST":
        if request.POST.get('key'):
            key = request.POST.get('key')
            remove_from_basket(request, product_name, key)
            add_to_basket(request, product_name)
            
            if request.user.is_authenticated:
                try:
                    customer = get_object_or_404(Customer, user=request.user)
                    order = get_object_or_404(Order, customer=customer, status='Pending')
                    remove_from_db_basket(order, key)
                    add_order_items(request,order)
                except:
                    pass
            return redirect('static_site:basket')
        else: 
            add_to_basket(request, product_name)
            if request.user.is_authenticated:
                try:                    
                    customer = get_object_or_404(Customer, user=request.user)
                    order = get_object_or_404(Order, customer=customer, status='Pending')
                    add_to_db_basket(request,product_name, order)   
                except: pass
    context = get_context(request, 'single', related_products)
    context.update({'product': product, "edit": edit})
    return render(request, 'static_site/single_product.html', context)


def basket(request, product_name="", key=""):
    if product_name and key:
        remove_from_basket(request, product_name, key)
        if request.user.is_authenticated:
            try:
                customer = get_object_or_404(Customer, user=request.user)
                order = get_object_or_404(Order, customer=customer, status='Pending')
                remove_from_db_basket(order, key)
            except: pass
        return redirect('static_site:basket')
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    context = get_context(request, 'basket', products)
    context.update({'total': total, 'deal': deal, 'subtotal': subtotal})
    return render(request, 'static_site/my_basket.html', context)


@login_required()
def checkout(request):
    #get customer or create new customer
    try: customer = get_object_or_404(Customer, user=request.user)
    except Http404: customer = Customer.objects.create(user=request.user)
    
    #get existing unplaced order from same user or create a new one
    try: order = get_object_or_404(Order, customer=customer, status='Pending')
    except Http404: order = Order.objects.create(customer=customer)
    
    #create order item object list for all the orders stored in session data
    order_items = add_order_items(request, order)
    print(order)
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    context = get_context(request, 'checkout', products)
    context.update({'total': total, 'deal': deal, 'subtotal': subtotal})
    return render(request, 'static_site/checkout.html', context)


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
    return redirect('static_site:checkout')