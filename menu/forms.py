from django import forms
from .models import Category

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['category_name', 'description']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name', 'description']

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)

    def clean_category_name(self):
        name = self.cleaned_data['category_name'].strip().title()

        if Category.objects.filter(
            vendor=self.vendor,
            category_name__iexact=name
        ).exists():
            raise forms.ValidationError("Category already exists.")

        return name