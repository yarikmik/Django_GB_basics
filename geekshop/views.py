from django.shortcuts import render
from geekshop.functions import get_json_data
from mainapp.views import get_basket

def index(request):
    title = 'магазин'
    context = {
        'title': title,
        'basket': get_basket(request.user),
    }
    # context = get_json_data('index')
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
        'basket': get_basket(request.user),
    }
    # context = get_json_data('contacts')
    return render(request, 'geekshop/contact.html', context)
