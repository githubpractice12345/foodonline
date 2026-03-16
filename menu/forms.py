from django import forms
from .models import Category, FoodItem
from accounts.validators import allow_only_images_validator
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from accounts.validators import allow_only_images_validator

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
    
# class FoodItemForm(forms.ModelForm):
#     image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
#     class Meta:
#         model = FoodItem
#         fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']





# class FoodItemForm(forms.ModelForm):
#     image = forms.FileField(
#         widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
#         validators=[allow_only_images_validator]
#     )

#     class Meta:
#         model = FoodItem
#         fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

#     def clean_food_title(self):
#         food_title = self.cleaned_data['food_title']
#         vendor = self.initial.get('vendor')

#         slug = slugify(food_title)

#         if FoodItem.objects.filter(vendor=vendor, slug__iexact=slug).exists():
#             raise ValidationError("Food item already exists for this vendor.")

#         return food_title



# class FoodItemForm(forms.ModelForm):

#     image = forms.FileField(
#         widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
#         validators=[allow_only_images_validator]
#     )

#     class Meta:
#         model = FoodItem
#         fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

#     def __init__(self, *args, vendor=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.vendor = vendor   # store vendor for validation

#     def clean_food_title(self):
#         food_title = self.cleaned_data.get('food_title')
#         slug = slugify(food_title)

#         if FoodItem.objects.filter(vendor=self.vendor, slug__iexact=slug).exists():
#             raise ValidationError("This food item already exists for this vendor.")

#         return food_title



class FoodItemForm(forms.ModelForm):

    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}),
        validators=[allow_only_images_validator]
    )

    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

    def __init__(self, *args, vendor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vendor = vendor

        #modify the form field 'category' to fetch or prnt only the category that belongs to loggedin user
        if vendor:
            self.fields['category'].queryset = Category.objects.filter(vendor=vendor)

    def clean_food_title(self):
        food_title = self.cleaned_data.get('food_title')
        slug = slugify(food_title)

        qs = FoodItem.objects.filter(
            vendor=self.vendor,
            slug__iexact=slug
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("This food item already exists for this vendor.")

        return food_title