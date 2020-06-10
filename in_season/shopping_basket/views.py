from django.shortcuts import render
from static_site.models import Category, Product, Phone_Number

# Create your views here.
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
        form = CheckoutForm(request.POST)
        if form.is_valid():
            complete_order(request, form)
            clear_basket(request)
    else:
        form = CheckoutForm()    
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