from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


def total_prise_in_basket(basket):
    total_price = 0
    for basket_object in basket:
        total_price += basket_object.total_price()
    return total_price


def total_quantity_in_basket(basket):
    total = 0
    for basket_object in basket:
        total += basket_object.quantity
    return total


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    related_products = Product.objects.all()[:4]
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'related_products': related_products,
            'products': products,
            'category': category,
            'basket': basket,
            'quantity': total_quantity_in_basket(basket),
            'total_price': total_prise_in_basket(basket),
        }
        return render(request, 'mainapp/products.html', context)

    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': related_products,
        'products': products,
        'basket': basket,
        'quantity': total_quantity_in_basket(basket),
        'total_price': total_prise_in_basket(basket),
    }
    return render(request, 'mainapp/products.html', context)
