from django.forms import ModelForm
from django import forms
from mainapp.models import ProductCategory, Product


class CategoryForm(ModelForm):

    discount = forms.IntegerField(
        label='скидка',
        required=False,
        min_value=0,
        max_value=90,
        initial=0,
    )

    class Meta:
        model = ProductCategory
        # fields = ('name', 'description')
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # выводит все поля модели
        exclude = ('is_active', )  #  исключения

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'
