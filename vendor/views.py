from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from vendor.forms import VendorForm, OpeningHourForm
from accounts.forms import UserProfileForm
from .models import Vendor, OpeningHour
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError
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
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
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
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
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
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')

#food CRUD
# #ADD
# def add_food(request):
#     if request.method == "POST":
#         form = FoodItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             foodtitle = form.cleaned_data['food_title']
#             food = form.save(commit=False)
#             food.vendor = get_vendor(request)
#             food.slug = slugify(foodtitle)
#             form.save()
#             messages.success(request, 'Food Item added successfully')
#             return redirect('fooditems_by_category', food.category.id)
#         else:
#             print(form.errors)
#     else:
#         form = FoodItemForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'vendor/add_food.html', context)



# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def add_food(request):
#     vendor = get_vendor(request)

#     if request.method == "POST":
#         form = FoodItemForm(request.POST, request.FILES, initial={'vendor': vendor})

#         if form.is_valid():
#             food = form.save(commit=False)
#             food.vendor = vendor
#             food.slug = slugify(food.food_title)
#             food.save()
#             messages.success(request, 'Food Item added successfully')
#             return redirect('fooditems_by_category', food.category.id)
#         else:
#             print(form.errors)
#     else:
#         form = FoodItemForm(initial={'vendor': vendor})
#     context = {
#         'form': form,
#     }
#     return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):

    vendor = get_vendor(request)

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, vendor=vendor)

        if form.is_valid():
            food = form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(food.food_title)
            food.save()

            messages.success(request, "Food Item added successfully")
            return redirect('fooditems_by_category', food.category.id)

        else:
            print(form.errors)

    else:
        form = FoodItemForm(vendor=vendor)

        #modify the form field 'category' to contain only the category that belongs to loggedin user.
        #form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
    context = {
        'form': form
    }

    return render(request, 'vendor/add_food.html', context)


# #EDIT
# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def edit_food(request, pk=None):
#         food = get_object_or_404(FoodItem, pk=pk)
#         if request.method == "POST":
#             form = FoodItemForm(request.POST, request.FILES, instance=food)
#             if form.is_valid():
#                 foodtitle = form.cleaned_data['food_title']
#                 food = form.save(commit=False)
#                 food.vendor = get_vendor(request)
#                 food.slug = slugify(foodtitle)
#                 food.save()
#                 messages.success(request, "Food Item updated successfully")
#                 return redirect("fooditems_by_category", food.category.id)
#             else:
#                 print(form.errors)
#         else:
#             form = FoodItemForm(instance=food)
#         context = {
#             'form': form,
#             'food': food
#         }
#         return render(request, 'vendor/edit_food.html', context)



# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def edit_food(request, pk=None):
#         food = get_object_or_404(FoodItem, pk=pk)
#         vendor = get_vendor(request)

#         if request.method == "POST":
#             form = FoodItemForm(request.POST, request.FILES, initial={'vendor': vendor}, instance=food)

#             if form.is_valid():
#                 foodtitle = form.cleaned_data['food_title']
#                 food = form.save(commit=False)
#                 food.vendor = vendor
#                 food.slug = slugify(foodtitle)
#                 food.save()

#                 messages.success(request, "Food Item updated successfully")
#                 return redirect("fooditems_by_category", food.category.id)

#         else:
#             form = FoodItemForm(initial={'vendor': vendor}, instance=food)
#         context = {
#             'form': form,
#             'food': food
#         }
#         return render(request, 'vendor/edit_food.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):

    vendor = get_vendor(request)

    # Ensure vendor can only edit their own food
    food = get_object_or_404(FoodItem, pk=pk, vendor=vendor)

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, vendor=vendor, instance=food)

        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(foodtitle)
            food.save()

            messages.success(request, "Food Item updated successfully")
            return redirect("fooditems_by_category", food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(vendor=vendor, instance=food)

    context = {
        'form': form,
        'food': food
    }

    return render(request, 'vendor/edit_food.html', context)


#DELETE
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category', food.category.id)


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor = get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)

def add_opening_hours(request):
    #handle the data sent from ajax request and save successfully to database.
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            #fetching the data from POST Request
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'closed'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                
                return JsonResponse(response)

            except IntegrityError:
                # response = {'status': 'failed', 'message': 'Opening hour already exists for this day.'}
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' Opening hour already exists for this day!'}
                return JsonResponse(response)

    else:
        HttpResponse('Invalid Request')

def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})
