from django.forms import ModelForm

from mainapp.models import ProductCategory


class CategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'




