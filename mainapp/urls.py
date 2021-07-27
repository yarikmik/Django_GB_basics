from django.urls import path, include
from .views import products
import geekshop.views as geekshop

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
]



