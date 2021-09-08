from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from adminapp.forms import CategoryForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import connection

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import F, Q


class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        title = 'админка/пользователи'
        context.update({'title': title})

        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        title = 'пользователи/создание'
        context.update({'title': title})

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        title = 'профиль'
        context.update({'title': title})

        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'objects'
    success_url = reverse_lazy('admin_staff:users')


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        title = 'админка/категории'
        context.update({'title': title})

        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        title = 'категории/создание'
        context.update({'title': title})

        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    # fields = '__all__'
    form_class = CategoryForm
    success_url = reverse_lazy('admin_staff:categories')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data()
        title = 'категория'
        context.update({'title': title})

        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1-discount/100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)



class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/categories_delete.html'
    context_object_name = 'objects'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = self.model.objects.filter(category__pk=self.kwargs['pk']).order_by('name')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        title = 'админка/продукт'
        context.update({'title': title})
        context.update({'category': category})
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_initial(self):
        return {
            'category': get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        title = 'продукт/создание'
        context.update({'title': title})
        return context

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs['pk']])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        title = 'продукт/редактирование'
        context.update({'title': title})
        return context

    def get_success_url(self):
        return reverse('admin_staff:products', args=[self.object.category_id])


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        product.is_active = False if product.is_active else True
        product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver (pre_save, sender=ProductCategory)
def products_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)