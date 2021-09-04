from django.shortcuts import render


def index(request):
    title = 'магазин'
    context = {
        'title': title,

    }
    # context = get_json_data('index')
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,

    }
    # context = get_json_data('contacts')
    return render(request, 'geekshop/contact.html', context)
