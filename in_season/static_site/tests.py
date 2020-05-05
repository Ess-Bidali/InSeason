from django.test import TestCase
from django.urls import reverse
from .models import Phone_Number, Order, OrderItem, Customer
from django.contrib.auth.models import User


class ParentUserTestCase(TestCase):
    fixtures = ['test_data.json', 'test_data2.json']

    def add_to_basket(self, product_name='onion', size='Small', quantity=2, key=''):
        path_name ='static_site:single_product'
        if key:
            post_args = {'size': size, 'quantity': quantity, 'key': key}
        else:
            post_args = {'size': size, 'quantity': quantity}
        url = reverse(path_name, kwargs={'product_name':product_name})
        return self.client.post(url, post_args, follow=True)

    def edit_product_in_basket(self, product_name='onion', original_size='Small', 
                                        new_size='Medium', new_quantity=2):
        key = f'{product_name}_{original_size}'
        response = self.add_to_basket(product_name=product_name,size=new_size, quantity=new_quantity, key=key)
        return response

    def remove_product(self):
        path_name = 'static_site:delete'
        product_name='onion'
        size = 'Small'
        key = f'{product_name}_{size}'
        url = reverse(path_name, kwargs={'product_name':product_name, 'key': key})
        return self.client.get(url)

class UnloggedUserCartTest(ParentUserTestCase):
    """Test suite for cart/basket functions for unlogged users"""
 
    def test_get_random_static_page(self):
        path_name = 'static_site:home'
        response = self.client.get(reverse(path_name))
        self.assertEqual(response.status_code, 200)


    def test_add_to_basket(self):
        original_customer_entries = len(Customer.objects.all())
        original_order_entries = len(Order.objects.all())
        original_order_item_entries = len(OrderItem.objects.all())
        product_name, size, quantity = 'onion', 'Small', 2
        response = self.add_to_basket()
        session = self.client.session
        key = {product_name: {f'{product_name}_{size}': quantity}}
        self.assertEqual(session['user_orders']['items'], key)
        self.assertEqual(response.templates[0].name, 'static_site/single_product.html')
        #Should not affect database
        self.assertEqual(len(Customer.objects.all()), (original_customer_entries))
        self.assertEqual(len(Order.objects.all()), (original_order_entries))
        self.assertEqual(len(OrderItem.objects.all()), (original_order_item_entries))
        

    def test_edit_basket(self):
        #Add product to session first        
        self.add_to_basket()
        #Then modify the product
        response = self.edit_product_in_basket()
        session = self.client.session
        product_name, new_size, new_quantity = 'onion', 'Medium', 2
        new_key = {product_name: {f'{product_name}_{new_size}': new_quantity}}
        self.assertEqual(response.context["nbar"], 'basket')
        self.assertEqual(response.templates[0].name, 'static_site/my_basket.html')
        self.assertEqual(session['user_orders']['items'], new_key)
        

    def test_remove_from_basket_with_other_items(self):
        #Add product to session first
        self.add_to_basket(product_name='tomatoe')
        self.add_to_basket()
        session = self.client.session
        number_of_items = len(session['user_orders']['items'])
        #Then remove the product
        response = self.remove_product()
        session = self.client.session
        number_of_items_after = len(session['user_orders']['items'])
        self.assertEqual(number_of_items_after, (number_of_items - 1))


    def empty_basket(self):
        #Add product to session first
        self.test_add_to_basket()
        #Then remove the product
        response = self.remove_product()
        session = self.client.session
        with self.assertRaises(KeyError): session['user_orders']


    def test_access_to_checkout(self):
        #Test whether unlogged user can access checkout page
        response = self.client.get(reverse('static_site:checkout'), follow=True)
        #Should redirect to login page
        self.assertEqual(response.templates[0].name, 'static_site/login.html')
    

    def test_register_user(self, email=''):
        original_entries_in_user_model = len(User.objects.all())
        #Create user
        path_name = 'static_site:register'
        url = reverse(path_name)
        username, password, phone = ('Aypol', 'aypoll1', '71234578')
        post_args = {'username': username, 'password':password, 'email':email, 'phone':phone}
        response = self.client.post(url, post_args)
        #Fetch user and test data
        user = User.objects.get(username__iexact=username)
        phone_num = Phone_Number.objects.get(number=phone)
        self.assertEqual(Phone_Number.objects.get(user=user).number, int(phone))
        self.assertEqual(user.phone_number.all()[0], phone_num)
        self.assertEqual(user.email, email)
        self.assertEqual(len(User.objects.all()), (original_entries_in_user_model + 1))
        

    def test_register_user_with_optionals(self):
        #Create user
        email = 'aypoll@gmail.com'
        response = self.test_register_user(email=email)        


    def test_login(self):
        username, password = 'Aypol', 'aypoll1'
        self.test_register_user()
        self.assertEqual(self.client.login(username=username, password=password), True)


    def test_logout(self):
        #Create user and login user
        username, password = 'Aypol', 'aypoll1'
        self.test_login()
        #Logged user with empty basket should be redirected to shop.html instead of login.html
        with self.assertRaises(AssertionError): self.test_access_to_checkout()
        #Logout
        self.client.logout()
        self.test_access_to_checkout()
        session = self.client.session
        with self.assertRaises(KeyError): session['user_orders']
        
        
class LoggedUserCartTest(ParentUserTestCase):
    """Test suite for cart/basket functions for unlogged users"""
    def setUp(self):
        self.username = 'test_user'
        self.password = 'testUser1'
        self.email = 'test_useruser@gmail.com'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.client.force_login(user=self.user)


    def test_user_logged_in(self):
        #First add product so checkout page doesn't redirect to shop
        response = self.add_to_basket()
        #Check if checkout page loads without redirecting
        response = self.client.get(reverse('static_site:checkout'))
        self.assertNotEqual(response.templates[0].name, 'static_site/login.html')
        self.assertEqual(response.templates[0].name, 'static_site/checkout.html')


    def test_user_add_to_basket(self):
        #Should increment number of entries by 1 in (Order, OrderItem, Customer)models 
        original_customer_entries = len(Customer.objects.all())
        original_order_entries = len(Order.objects.all())
        original_order_item_entries = len(OrderItem.objects.all())
        response = self.add_to_basket()
        self.assertEqual(len(Customer.objects.all()), (original_customer_entries + 1))
        self.assertEqual(len(Order.objects.all()), (original_order_entries + 1))
        self.assertEqual(len(OrderItem.objects.all()), (original_order_item_entries + 1))


    def test_user_edit_basket(self):
        #Add product first
        self.add_to_basket()
        customer = Customer.objects.get(user=self.user)
        order = Order.objects.get(customer=customer)
        original_order_item = OrderItem.objects.get(order=order)
        original_order_item_entries = len(OrderItem.objects.all())        
        #Then modify the product
        response = self.edit_product_in_basket()
        session = self.client.session
        product_name, new_size, new_quantity = 'onion', 'Medium', 2
        #Tests
        new_order_item = OrderItem.objects.get(order=order)
        self.assertNotEqual(original_order_item, new_order_item)
        self.assertEqual(len(OrderItem.objects.all()), original_order_item_entries)


    def test_user_remove_from_basket(self):
        #Add product to session first
        self.add_to_basket()
        customer = Customer.objects.get(user=self.user)
        order = Order.objects.get(customer=customer)
        num_of_orders_1 = len(Order.objects.filter(customer=customer))
        original_order_item = OrderItem.objects.get(order=order)
        self.assertIn(original_order_item, OrderItem.objects.all())
        #Then remove the product
        response = self.remove_product()
        #Tests
        #Should affect database
        self.assertNotIn(original_order_item, OrderItem.objects.all())
        num_of_orders_2 = len(Order.objects.filter(customer=customer))
        self.assertEqual(num_of_orders_1, (num_of_orders_2 + 1))