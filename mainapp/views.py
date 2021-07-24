from django.shortcuts import render
from mainapp.models import ProductCategory, Product
from geekshop.functions import get_json_products_data


def index(request):
    title = 'каталог'
    links_menu = ProductCategory.objects.all()
    related_products = Product.objects.all()[:4]

    # products_data_from_json = get_json_products_data('geekshop/json_products_data.json')
    #
    # database = Product.objects.all()
    # name_list = [i.name for i in database]
    #
    # for product in products_data_from_json:
    #     cat = ProductCategory.objects.get(name=product['category'].title())
    #     if product['name'] not in name_list:
    #         new_product = Product(
    #             category=cat,
    #             name=product['name'],
    #             short_desc=product['short_desc'],
    #             price=product['price'],
    #             quantity=product['quantity'],
    #         )
    #         new_product.save()

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': related_products
    }
    return render(request, 'mainapp/products.html', context)
