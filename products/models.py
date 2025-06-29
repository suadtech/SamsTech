from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import json


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
class Product(models.Model):
    class Meta:
        ordering = ['name']
        device_tier = models.CharField(max_length=254, null=True, blank=True)

        extra_data = models.JSONField(default=dict, blank=True, null=True)
        
    
    # Basic fields
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    sku = models.CharField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    
    # All the extra fields from your fixture
    brand = models.CharField(max_length=254, null=True, blank=True)
    shipping = models.CharField(max_length=254, null=True, blank=True)
    estimated_delivery = models.CharField(max_length=254, null=True, blank=True)
    vat_status = models.CharField(max_length=254, null=True, blank=True)
    stock_status = models.CharField(max_length=254, null=True, blank=True)
    warranty = models.CharField(max_length=254, null=True, blank=True)
    compatibility = models.CharField(max_length=254, null=True, blank=True)
    includes = models.CharField(max_length=254, null=True, blank=True)
    condition = models.CharField(max_length=254, null=True, blank=True)
    availability = models.CharField(max_length=254, null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    display_type = models.CharField(max_length=254, null=True, blank=True) 
    release_year = models.CharField(max_length=254, null=True, blank=True)
    device_tier = models.CharField(max_length=254, null=True, blank=True)  
    extra_data = models.JSONField(default=dict, blank=True, null=True)
    color = models.CharField(max_length=254, null=True, blank=True) 
    size = models.CharField(max_length=254, null=True, blank=True)
    weight = models.CharField(max_length=254, null=True, blank=True)
    dimensions = models.CharField(max_length=254, null=True, blank=True)
    material = models.CharField(max_length=254, null=True, blank=True)
    model_number = models.CharField(max_length=254, null=True, blank=True)
   
    # System fields
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
