from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse


#helper method for returning a json response when method is ajax views.shop()
def filter_results(products):
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
    print(request.session['user_orders']['items'])


#helper to remove items from basket
def remove_from_basket(request, product_name, key):
    if product_name in request.session['user_orders']['items']:
        if key in request.session['user_orders']['items'][product_name]:
            del request.session['user_orders']['items'][product_name][key]
            if is_empty(request, product_name):
                del request.session['user_orders']['items'][product_name]
            request.session.modified = True
        

def items_in_basket(request):
    if 'user_orders' not in request.session:
        return []
    ans = [product for product in request.session['user_orders']['items'].keys()]
    return ans


def specific_items(request):
    if 'user_orders' not in request.session:
        return {}
    return request.session['user_orders']['items']

def is_empty(request, product_key):
    return not request.session['user_orders']['items'][product_key]