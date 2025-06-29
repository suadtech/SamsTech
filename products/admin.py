from django.contrib import admin
from .models import Category, Product
from django.db import models 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'friendly_name']
    search_fields = ['name', 'friendly_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'rating']
    list_filter = ['category']
    search_fields = ['name', 'sku', 'description',]
    list_editable = ['price']
    readonly_fields = ['sku']
    
    fields = ['name', 'sku', 'category', 'description', 'price', 'rating',
              'image', 'image_url', 'brand', 'shipping', 'warranty',
              'excludes', 'specifications', 'tags', 'category_path']
              
              
    excludes = models.CharField(max_length=254, null=True, blank=True)
    specifications = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=254, null=True, blank=True)
    category_path = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
