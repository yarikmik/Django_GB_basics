from django.urls import path, include
from .views import index
import geekshop.views as geekshop

urlpatterns = [
    path('', index),
]



