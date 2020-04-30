from decimal import *
from django.http import Http404
from .forms import CustomerDetailsForm
from django.contrib.auth.models import User
from .logged_user_functions import complete_order
from .models import Category, Product, Phone_Number
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .static_helper_functions import get_json_respose, paginate, get_context
from .helper_functions import add_to_basket, remove_from_basket, get_total_cost, clear_basket, edit_basket_item, add_all_orders_to_db

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
        categ_object = Category.objects.filter(name__iexact=category)[0]
        products = categ_object.product_set.all() #all products contained in this category

        #if request is ajax, return filtered products as a json object
        if request.is_ajax(): return get_json_respose(products)            
    else:
        products = Product.objects.all()
    categs = Category.objects.all() #all categories
    products = paginate(request, products)
    context = get_context(request, 'shop', products)
    context.update({'categs': categs, 'filtr': category})
    return render(request, 'static_site/shop.html', context)


def single(request, product_name, edit=""):
    product = get_object_or_404(Product,name__iexact=product_name)    
    if request.method == "POST":
        # If a key has been passed then it is an edit request
        if request.POST.get('key'):
            product_key = request.POST.get('key')
            edit_basket_item(request, product_name, product_key)
            return redirect('static_site:basket')

        # If there is no key, then simply add item to basket
        else: 
            add_to_basket(request, product_name) 
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    context = get_context(request, 'single', related_products)
    context.update({'product': product, "edit": edit})
    return render(request, 'static_site/single_product.html', context)


def basket(request, product_name="", key=""):
    if product_name and key:
        remove_from_basket(request, product_name, key)        
        return redirect('static_site:basket')
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    context = get_context(request, 'basket', products)
    context.update({'total': total, 'deal': deal, 'subtotal': subtotal})
    return render(request, 'static_site/my_basket.html', context)


@login_required()
def checkout(request):
    if request.method == 'POST':
        #validate input and addign to variables
        form = CustomerDetailsForm(request.POST)
        if form.is_valid():
            complete_order(request, form)
            clear_basket(request)
    else:
        form = CustomerDetailsForm()    
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    #if any product order was placed, redirect to shop else, go to checkout
    if not products: return redirect('static_site:shop')
    #create order item object list for all the orders stored in session data
    order_items = add_all_orders_to_db(request)        
    context = get_context(request, 'checkout', products)
    context.update({'total': total, 'deal': deal, 'subtotal': subtotal, 'form':form})
    return render(request, 'static_site/checkout.html', context)


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username') if request.POST.get('username') else ''
        password = request.POST.get('password') if request.POST.get('password') else ''
        email = request.POST.get('email') if request.POST.get('email') else ''
        phone_number = request.POST.get('phone') if request.POST.get('phone') else ''
        if username and password:
            user = User.objects.create_user(username, password=password)
            if phone_number:
                phone_number = Phone_Number.objects.create(user=user, number=phone_number)                
            if email: 
                user.email = email
            user.save()
            login(request, user)
    return redirect('static_site:checkout')