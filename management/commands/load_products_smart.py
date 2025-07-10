from django.core.management.base import BaseCommand
from django.core import serializers
from products.models import Product
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/fixtures/products.json', 'r') as f:
            data = json.load(f)
        
        for item in data:
            fields = item['fields']
            # Extract known fields
            product_data = {
                'name': fields.get('name'),
                'price': fields.get('price'),
                'description': fields.get('description'),
                'brand': fields.get('brand'),
                'category': fields.get('category'),
                'sku': fields.get('sku'),
                'rating': fields.get('rating'),
                'image_url': fields.get('image_url'),
                'shipping': fields.get('shipping'),
                'estimated_delivery': fields.get('estimated_delivery'),
                'vat_status': fields.get('vat_status'),
                'fixture_data': fields  # Store all data in JSON
            }
            Product.objects.create(**{k:v for k,v in product_data.items() if v is not None})
        
        self.stdout.write(f'Successfully loaded {len(data)} products')
