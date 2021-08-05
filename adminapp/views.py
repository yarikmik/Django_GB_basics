from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import CategoryForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test


def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'objects': users_list,
    }
    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_update(request, id):
    title = 'профиль'
    user = ShopUser.objects.get(id=id)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserEditForm(instance=user)

    context = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, id):
    user = ShopUser.objects.filter(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('admin_staff:users'))


@user_passes_test(lambda u: u.is_superuser)  # для контроля входа, только пользователи с флагом is_superuser
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    else:
        category_form = CategoryForm()

    context = {
        'title': title,
        'update_form': category_form
    }

    return render(request, 'adminapp/categories_update.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_update(request, pk):
    title = 'категория'
    # user = ShopUser.objects.get(id=id)
    category = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        edit_form = CategoryForm(request.POST, request.FILES, instance=category)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        edit_form = CategoryForm(instance=category)

    context = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/categories_update.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_delete(request, pk):
    category = ProductCategory.objects.filter(pk=pk)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:categories'))


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
