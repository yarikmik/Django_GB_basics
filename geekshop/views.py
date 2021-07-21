from django.shortcuts import render
from geekshop.functions import get_json_data


def index(request):
    context = get_json_data('index')
    return render(request, 'geekshop/index.html',context)


def contacts(request):
    context = get_json_data('contacts')
    return render(request, 'geekshop/contact.html', context)
