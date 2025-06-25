from django.db import models

class Product(models.Model):

    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)
    
    shipping = models.CharField(max_length=100, blank=True, null=True)
    estimated_delivery = models.CharField(max_length=50, blank=True, null=True)
    vat_status = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True) 

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
