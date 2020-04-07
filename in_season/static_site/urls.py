from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'static_site'

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:category>', views.shop, name='shop'),
    path('shop/product/<str:product_name>', views.single, name='single_product'),
    path('shop/basket/', views.basket, name='basket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)