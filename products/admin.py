from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'friendly_name']
    search_fields = ['name', 'friendly_name']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'rating', 'image']
    list_filter = ['category']
    search_fields = ['name', 'sku', 'description']
    list_editable = ['price']
    readonly_fields = ['sku']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'category', 'description')
        }),
        ('Pricing & Rating', {
            'fields': ('price', 'rating')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('Additional Details', {
            'fields': ('brand', 'shipping', 'warranty'),
            'classes': ('collapse',)
        }),
    )
