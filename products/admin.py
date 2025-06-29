from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'friendly_name']
    search_fields = ['name', 'friendly_name']
    prepopulated_fields = {'name': ('friendly_name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'rating']
    list_filter = ['category']
    search_fields = ['name', 'sku', 'description']
    list_editable = ['price']
    readonly_fields = ['sku']
