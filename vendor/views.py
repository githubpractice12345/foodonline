from django.shortcuts import render, get_object_or_404, redirect
from vendor.forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
# Create your views here.

#helper function for reusing and also can create this inside a utils.py in vendor app and reuse by importing.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings/profile updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    # vendor = Vendor.objects.get(user=request.user)
    vendor = get_vendor(request)
    # categories = Category.objects.filter(vendor=vendor)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at') #for making category in order even after edit.
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    # vendor = Vendor.objects.get(user=request.user)
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    # print(fooditems)
    context = {
        'fooditems': fooditems,
        'category': category,
    }

    return render(request, 'vendor/fooditems_by_category.html', context)


#Category CRUD

#CREATE/ADD
# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category_name = form.cleaned_data['category_name']
#             category = form.save(commit=False)
#             category.vendor = get_vendor(request)
#             category.slug = slugify(category_name)
#             category.save()

#             messages.success(request, 'Category added successfully')
#             return redirect('menu_builder')
#         else:
#             print(form.errors)
#     else:
#         form = CategoryForm()

#     return render(request, 'vendor/add_category.html', {'form': form})

#We pass vendor in form because we have to validate in forms.py
def add_category(request):

    vendor = get_vendor(request)

    if request.method == "POST":
        form = CategoryForm(request.POST, vendor=vendor)

        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category.category_name)
            category.save()

            messages.success(request, "Category added successfully")
            return redirect("menu_builder")

    else:
        form = CategoryForm(vendor=vendor)
    
    return render(request, "vendor/add_category.html", {"form": form})


# from django.db import IntegrityError
# from django.utils.text import slugify

# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)

#         if form.is_valid():
#             category = form.save(commit=False)
#             category.vendor = get_vendor(request)
#             category.slug = slugify(category.category_name)

#             try:
#                 category.save()
#                 messages.success(request, 'Category added successfully')
#                 return redirect('menu_builder')

#             except IntegrityError:
#                 messages.error(request, 'Category already exists for this vendor.')

#     else:
#         form = CategoryForm()

#     return render(request, 'vendor/add_category.html', {'form': form})


#EDIT
def edit_category(request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        vendor = get_vendor(request)

        if request.method == "POST":
            form = CategoryForm(request.POST, vendor=vendor, instance=category)

            if form.is_valid():
                category = form.save(commit=False)
                category.vendor = vendor
                category.slug = slugify(category.category_name)
                category.save()

                messages.success(request, "Category updated successfully")
                return redirect("menu_builder")

        else:
            form = CategoryForm(vendor=vendor, instance=category)
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'vendor/edit_category.html', context)


# def edit_category(request, pk=None):
#     category = get_object_or_404(Category, pk=pk, vendor=get_vendor(request))  # Filter by vendor for security
#     vendor = get_vendor(request)

#     if request.method == "POST":
#         form = CategoryForm(request.POST, instance=category, vendor=vendor)  # instance= for UPDATE (not isinstance)

#         if form.is_valid():
#             form.save()  # Saves directly (updates existing instance); no need for commit=False/vendor/slug
#             messages.success(request, "Category updated successfully")
#             return redirect("menu_builder")

#     else:
#         form = CategoryForm(instance=category, vendor=vendor)  # instance= pre-fills form

#     context = {
#         'form': form,
#         'category': category,  # Optional: for custom action if needed
#         'pk': pk,  # Pass pk explicitly for template
#     }
#     return render(request, 'vendor/edit_category.html', context)

#DELETE
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')