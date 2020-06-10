from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Order, Customer

#commonly requested context parameter for all views
def get_capacity(in_basket):
    capacity = 0
    for value in in_basket.values():
        for val in value.values():
            capacity += 1
    return capacity

#common context parameters
def get_context(request, n_bar='home', products=''):
    if not products: products = {}
    in_basket = specific_items(request)
    capacity = get_capacity(in_basket)
    context = {'nbar': n_bar, 'products': products, 'in_basket': in_basket, 'capacity': capacity}
    return context


#returns a json response when method is ajax views.shop()
def get_json_respose(products):
    data = serializers.serialize('json', products)
    return JsonResponse(data, safe=False)

# Create paginate object for product list
def paginate(request, products):
    #initialize Paginator object with products and limit of items per page as parameters
    paginator = Paginator(products, 12) 
    #set requested page number, else set page to 1
    page = request.GET.get('page') if request.GET.get('page') else 1
    return paginator.get_page(page)

# Get products ordered by unlogged/anonymous user
def specific_items(request):
    if request.user.is_authenticated:
        try: customer = get_object_or_404(Customer, user=request.user)
        except Http404: customer = Customer.objects.create(user=request.user)
        #get existing unplaced order from same user or create a new one
        try: order = get_object_or_404(Order, customer=customer, status='Pending')
        except Http404: return {}
        items, total, deal = order.get_total()
        return items
    if 'user_orders' not in request.session:
        return {}
    return request.session['user_orders']['items']