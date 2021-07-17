from django.shortcuts import render
from geekshop.functions import get_json_data

def index(request):
    context = get_json_data('products')
    return render(request, 'mainapp/products.html', context)
