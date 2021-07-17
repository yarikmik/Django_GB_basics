from django.urls import path, include
from .views import index
import geekshop.views as geekshop

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
]



