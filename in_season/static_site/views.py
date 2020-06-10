import json
import base64
from datetime import datetime
from decimal import *
from django.http import Http404
from .forms import CheckoutForm
from django.contrib.auth.models import User
from .logged_user_functions import complete_order
from .models import Category, Product, Phone_Number, Stock
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .static_helper_functions import get_json_respose, paginate, get_context
from .helper_functions import add_to_basket, remove_from_basket, get_total_cost, clear_basket, edit_basket_item, add_all_orders_to_db


import requests
from requests.auth import HTTPBasicAuth



DEAL_OF_THE_DAY = 'avocado'
DISCOUNT = Decimal('3.00')

def index(request):
    products = Product.objects.all()[:4]
    deal = get_object_or_404(Product, name__iexact=DEAL_OF_THE_DAY)
    context = get_context(request, 'home', products)
    context.update({'deal': deal})
    return render(request, 'static_site/index.html', context)

def test_page(request):
    context = get_context(request, 'home')
    return render(request, 'static_site/test.html', context)

#static pages
def static_pages(request, page):
    context = get_context(request, 'home')
    if page == 'terms-and-conditions': return render(request, 'static_site/terms.html', context)
    elif page == 'privacy-policy': return render(request, 'static_site/privacy_policy.html', context)
    elif page == 'FAQs': return render(request, 'static_site/faqs.html', context)
    else : return redirect('static_site:home')


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
        if request.POST.get('key'):
        # If a key has been passed then it is an edit request
            product_key = request.POST.get('key')
            edit_basket_item(request, product_name, product_key)
            return redirect('static_site:my_basket')
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
        return redirect('static_site:my_basket')
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    context = get_context(request, 'basket', products)
    context.update({'total': total, 'deal': deal, 'subtotal': subtotal})
    return render(request, 'static_site/my_basket.html', context)


@login_required()
def checkout(request):
    if request.method == 'POST':
        #validate input and adding to variables
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if request.POST.get('payment') == 'Pay now': process_payment(request)
            complete_order(request, form)
            clear_basket(request)
    else:
        form = CheckoutForm()    
    order_items = add_all_orders_to_db(request)
    products, subtotal, deal, total = get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT)
    #if any product order was placed, redirect to shop else, go to checkout
    if not products: return redirect('static_site:shop')
    #create order item object list for all the orders stored in session data            
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


def process_payment(request):
    # Authenticate, i.e. get access token
    access_token = get_mpesa_auth()
    credentials_expiry = '2020-05-10T11:10:03+03:00'
    short_code = '174379'
    timestamp = get_timestamp()
    lnm_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    password = encode_password(short_code, lnm_passkey, timestamp)
    transaction_type = ['CustomerPayBillOnline', 'CustomerBuyGoodsOnline']
    amount = request.POST.get('pay_amount')    
    phone_number = '254708374149'
    callback_url = ''
    account_ref = ''
    description = ''
    
    headers = { f'Authorization": "Bearer {access_token}'}

    request = {
        "BusinessShortCode": f"{short_code}",
        "password": f"{password}",
        "Timestamp": f"{timestamp}",
        "TransactionType": f"{transaction_type}",
        "Amount": f'{amount}',
        "PartyA": f"{phone_number}",
        "PartyB": f"{short_code}",
        "PhoneNumber": f"{phone_number}",
        "CallBackURL": f"{callback_url}",
        "AccountReference": f"{account_ref}",
        "TransactionDesc": f"{description}"
    }

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
  
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)


def get_timestamp():
    now = datetime.now()
    now = f'{now.strftime("%Y%m%d%H%M%S")}' #YYMMDDHHmmss (Time is 24hr-based)
    return now

def encode_password(shortcode, lnm_passkey, timestamp):
    password = f'{shortcode}{lnm_passkey}{timestamp}'
    password_in_bytes = password.encode('ascii')
    password = base64.b64encode(password_in_bytes)
    return password

def get_mpesa_auth():
    consumer_key = "pcj9rupHg2LUpiPUtT5AEMhTTn3y40de"
    consumer_secret = "7MwTgzhgZivUz9A4"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    json_data = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    json_data = json.loads(json_data.text)  # Converts returned json object into a python dictionary object
    access_token = json_data.get("access_token")
    print(access_token)
    return access_token