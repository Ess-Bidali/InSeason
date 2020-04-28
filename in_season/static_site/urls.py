from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'static_site'

urlpatterns = [
    
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:category>', views.shop, name='shop'),
    path('shop/product/<str:product_name>', views.single, name='single_product'),
    path('shop/product/<str:product_name>/<str:edit>', views.single, name='single_product_edit'),
    path('shop/basket/', views.basket, name='basket'),
    path('shop/basket/<str:product_name>/<str:key>', views.basket, name='basket'),
    path('shop/checkout/', views.checkout, name='checkout'),
# Account settings/pages 
    path('accounts/login/', auth_views.LoginView.as_view(template_name='static_site/login.html'), name='login'),
    path('accounts/register/', views.register_user, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='static_site:home'), name='logout'),
    path('accounts/switch/', auth_views.logout_then_login, name='switch_user'),
# Static pages
     path('<str:page>/', views.static_pages, name='static'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)