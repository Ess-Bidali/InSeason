# HELPER METHODS FOR LOGGED USER AND MODEL/DATABASE ACCESS
from .static_helper_functions import specific_items
from .models import Product, Order, OrderItem, Phone_Number, Customer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404


def get_order(request):
    try: customer = get_object_or_404(Customer, user=request.user)
    except Http404: return
    #get existing unplaced order from same user or terminate
    try: order = get_object_or_404(Order, customer=customer, status='Pending')
    except Http404: return
    return order


def get_or_create_order(request):
    try: customer = get_object_or_404(Customer, user=request.user)
    except Http404: customer = Customer.objects.create(user=request.user)
    #get existing unplaced order from same user or create a new one
    try: order = get_object_or_404(Order, customer=customer, status='Pending')
    except Http404: 
        order = Order.objects.create(customer=customer)
    return order


def get_basket_total(request):
    order = get_order(request)
    if not order: return {}, 0, 0
    order_items = OrderItem.objects.filter(order=order)
    products, total, deal = order.get_total()
    return products, total, deal


def add_to_db_basket(request, product_name, order_obj, detail='', quantity=''):
    product = Product.objects.get(name__iexact=product_name)
    if not detail or not quantity:
        quantity = int(request.POST.get('quantity'))
        detail = request.POST.get('size')    
    try: 
        order_item = get_object_or_404(OrderItem, order=order_obj, product=product, details=detail)
        order_item.quantity += quantity
    except Http404: 
        order_item = OrderItem.objects.create(order=order_obj, product=product, details=detail)
        order_item.quantity = quantity
    order_item.save()
    return order_item


def remove_from_db_basket(order, key, action=''):
    if not action: action = 'edit'
    product_name = key.split('_')[0]    
    product = get_object_or_404(Product, name__iexact=product_name)
    details = key.split('_')[1]
    order_item = get_object_or_404(OrderItem, order=order, product=product, details=details)
    order_item.delete()
    if action == 'delete' and not OrderItem.objects.filter(order=order):
        order.delete()


def complete_order(request, form):
    order = get_order(request)
    if not order: return
    fullname = f"{form.cleaned_data['first_name']}_{form.cleaned_data['last_name']}"
    location = f"{form.cleaned_data['additional_description']}, {form.cleaned_data['street_address']}, {form.cleaned_data['delivery_route']}, {form.cleaned_data['county']}"
    phone_number = form.cleaned_data['phone_number']
    try: phone_number = get_object_or_404(Phone_Number, number=phone_number)
    except: phone_number = Phone_Number.objects.create(user=request.user, number=phone_number)
    order.addressee, order.location, order.contact = (fullname, location, phone_number)
    order.status, order.is_ordered = ('Placed', True)
    order.save()


def get_product(product_name):
    return Product.objects.get(name__iexact=product_name)