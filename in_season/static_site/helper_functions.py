from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse, Http404
from .models import Product, OrderItem
from django.shortcuts import get_object_or_404


#common context parameters
def get_context(request, n_bar='home', products={} ):
    in_basket = specific_items(request)
    capacity = get_capacity(in_basket)
    context = {'nbar': n_bar, 'products': products, 'in_basket': in_basket, 'capacity': capacity}
    return context

#helper method for returning a json response when method is ajax views.shop()
def get_json_respose(products):
    data = serializers.serialize('json', products)
    return JsonResponse(data, safe=False)


#helper method for views.shop() to create paginate object
def paginate(request, products):
    #initialize Paginator object with products and limit of items per page as parameters
    paginator = Paginator(products, 12) 
    #set requested page number, else set page to 1
    page = request.GET.get('page') if request.GET.get('page') else 1
    return paginator.get_page(page)


#helper method for adding products to cart in views.index(), views.shop(), views.single()
def add_to_basket(request, product_name):
    how_many = int(request.POST.get('quantity')) if request.POST.get('quantity') else 1
    size = request.POST.get('size') if request.POST.get('size') else "Small"
    # del request.session['user_orders']
    # create user orders key if it doesnt exist
    if 'user_orders' not in request.session:
        user_details = {'name': 'Unregistered user', 'items': {}, 'location' : 'Kenya', 'contact': ""}
        request.session['user_orders'] =  user_details
    #if absent, add product as a key in the items dictionary
    if product_name not in request.session['user_orders']['items']:
        add_product = {product_name: {}}
        request.session['user_orders']['items'].update(add_product)
    #if absent, add product_Size as a key in the product dictionary to hold order quantity
    product_key = f'{product_name}_{size}'
    if product_key not in request.session['user_orders']['items'][product_name]:
        temporary_order = {product_key: 0}
        request.session['user_orders']['items'][product_name].update(temporary_order)
    #then update the number of items
    request.session['user_orders']['items'][product_name][product_key] += how_many
    request.session.modified = True


def add_to_db_basket(request, product_name, order_obj):
    quantity = int(request.POST.get('quantity'))
    detail = request.POST.get('size')
    product = Product.objects.get(name__iexact=product_name)
    try: 
        order_item = get_object_or_404(OrderItem, order=order_obj, product=product, details=detail)
    except Http404: 
        order_item = OrderItem.objects.create(order=order_obj, product=product, details=detail)
    order_item.quantity = quantity
    order_item.save()

#helper to remove items from basket
def remove_from_basket(request, product_name, key):
    if product_name in request.session['user_orders']['items']:
        if key in request.session['user_orders']['items'][product_name]:
            del request.session['user_orders']['items'][product_name][key]
            if is_empty(request, product_name):
                del request.session['user_orders']['items'][product_name]
            if not request.session['user_orders']['items']:
                del request.session['user_orders']
            request.session.modified = True


def remove_from_db_basket(order, key):
    product_name = key.split('_')[0]
    product = get_object_or_404(Product, name__iexact=product_name)
    details = key.split('_')[1]
    order_item = get_object_or_404(OrderItem, order=order, product=product, details=details)
    print(order_item)
    print(order_item.delete())


def specific_items(request):
    if 'user_orders' not in request.session:
        return {}
    return request.session['user_orders']['items']


def get_capacity(in_basket):
    capacity = 0
    for key,value in in_basket.items():
        for key, val in value.items():
            capacity += 1
    return capacity

def get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT):
    in_basket = specific_items(request)
    total = 0
    products = {}
    deal = 0
    for product_name, value in in_basket.items():
        prod = Product.objects.get(name__iexact=product_name)
        products.update({prod:value})
        if product_name == DEAL_OF_THE_DAY:
            deal += [val for val in value.values()][0] * DISCOUNT
        total += [val for val in value.values()][0] * prod.current_price
    subtotal = total + deal
    return products, subtotal, deal, total


def is_empty(request, product_key):
    return not request.session['user_orders']['items'][product_key]


def add_order_items(request, order_obj):
    order_requests = specific_items(request)
    order_items = []
    for product_name,values in order_requests.items():
        for specific,val in values.items():
            detail = specific.split('_')[1]
            product = Product.objects.get(name__iexact=product_name)
            try: 
                order_item = get_object_or_404(OrderItem, order=order_obj, product=product, details=detail)
            except Http404: 
                order_item = OrderItem.objects.create(order=order_obj, product=product, details=detail)
            order_item.quantity = val
            order_item.save()
            order_items.append(order_item)
            print(order_items)
    return order_items