from django.core import serializers
from django.http import JsonResponse, Http404
from .logged_user_functions import add_to_db_basket, remove_from_db_basket, get_or_create_order, get_product, get_basket_total, get_order
from .static_helper_functions import specific_items


#       HELPER METHODS FOR CART FUNCTIONALITIES WHEN USER IS NOT LOGGED IN

#helper method for adding products to cart in views.index(), views.shop(), views.single()
def add_to_basket(request, product_name):
    how_many = int(request.POST.get('quantity')) if request.POST.get('quantity') else 1
    size = request.POST.get('size') if request.POST.get('size') else "Small"
    
    # create user orders key if it doesnt exist in request.session
    if 'user_orders' not in request.session:
        user_details = {'name': 'Unregistered user', 'items': {}, 'location' : 'Kenya', 'contact': ""}
        request.session['user_orders'] =  user_details

    #if absent, add the product name as a key in the items dictionary
    if product_name not in request.session['user_orders']['items']:
        add_product = {product_name: {}}
        request.session['user_orders']['items'].update(add_product)

    #if absent, add product_Size as a key in the product dictionary to hold order quantity as its value
    product_key = f'{product_name}_{size}'
    if product_key not in request.session['user_orders']['items'][product_name]:
        temporary_order = {product_key: 0}
        request.session['user_orders']['items'][product_name].update(temporary_order)

    #then update the number of items and save session changes
    request.session['user_orders']['items'][product_name][product_key] += how_many
    request.session.modified = True
    if request.user.is_authenticated:
        order = get_or_create_order(request)
        add_to_db_basket(request,product_name, order)


def edit_basket_item(request, product_name, product_key):
    action = 'edit'
    remove_from_basket(request, product_name, product_key, action)
    add_to_basket(request, product_name)


#helper to remove items from basket
def remove_from_basket(request, product_name, key, action=''):
    if not action: action = 'delete'   
    if product_name in request.session['user_orders']['items']:
        if key in request.session['user_orders']['items'][product_name]:
            del request.session['user_orders']['items'][product_name][key]
            if is_empty(request, product_name):
                del request.session['user_orders']['items'][product_name]
            if not request.session['user_orders']['items']:
                del request.session['user_orders']
            request.session.modified = True
    if request.user.is_authenticated:
        order = get_order(request)
        if not order: return
        remove_from_db_basket(order, key, action)
    

def clear_basket(request):
    del request.session['user_orders']


def get_total_cost(request, DEAL_OF_THE_DAY, DISCOUNT):
    total = 0
    products = {}
    deal = 0
    if request.user.is_authenticated:
        products, total, deal = get_basket_total(request)
    else:
        in_basket = specific_items(request)
        for product_name, value in in_basket.items():
            prod = get_product(product_name)
            products.update({prod:value})
            if product_name == DEAL_OF_THE_DAY:
                deal += [val for val in value.values()][0] * DISCOUNT
            total += [val for val in value.values()][0] * prod.current_price
    subtotal = total + deal
    return products, subtotal, deal, total


def is_empty(request, product_key):
    return not request.session['user_orders']['items'][product_key]


def add_all_orders_to_db(request):
    order_obj = get_or_create_order(request)
    order_requests = specific_items(request)
    order_items = []
    for product_name, values in order_requests.items():
        for specific,quantity in values.items():
            detail = str(specific).split('_')[1]
            order_item = add_to_db_basket(request, product_name, order_obj, detail, quantity)
            order_items.append(order_item)
    return order_items
