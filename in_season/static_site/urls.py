from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'static_site'

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<str:category>', views.shop, name='shop'),
    path('shop/<str:category>/', views.filter_results, name='filter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)