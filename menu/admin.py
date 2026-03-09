from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')
    list_filter = ('vendor',)
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vendor')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'vendor', 'category', 'price', 'updated_at', 'is_available')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name')
    list_filter = ('vendor', 'category', 'is_available')
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vendor', 'category')

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
