from django.core.management.base import BaseCommand
from products.models import Product
import json
import os

class Command(BaseCommand):
    help = 'Loads products from products.json, storing extra fields in JSONField.'

    def handle(self, *args, **options):
        fixture_path = os.path.join('products', 'fixtures', 'products.json')
        if not os.path.exists(fixture_path):
            self.stderr.write(self.style.ERROR(f"Fixture file not found: {fixture_path}"))
            return

        with open(fixture_path, 'r') as f:
            data = json.load(f)
        
        # Clear existing products to avoid duplicates if running multiple times
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared existing products."))

        loaded_count = 0
        for item in data:
            fields = item['fields']
            
            # Extract known fields that are explicitly defined in your model
            # You might need to adjust these based on your current models.py
            product_data = {
                'name': fields.pop('name', None),
                'price': fields.pop('price', None),
                'description': fields.pop('description', None),
                'category': fields.pop('category', None), # Assuming category is a CharField for now
                'brand': fields.pop('brand', None),
                'sku': fields.pop('sku', None),
                'image': fields.pop('image', None),
                'image_url': fields.pop('image_url', None),
                'rating': fields.pop('rating', None),
                'shipping': fields.pop('shipping', None),
                'estimated_delivery': fields.pop('estimated_delivery', None),
                'vat_status': fields.pop('vat_status', None),
                # Add any other fields that are explicitly in your Product model here
            }
            
            # Clean up None values and store remaining fields in fixture_data
            product_data = {k:v for k,v in product_data.items() if v is not None}
            product_data['fixture_data'] = fields # Store all remaining fields here

            try:
                Product.objects.create(**product_data)
                loaded_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error loading product {product_data.get('name', 'Unknown')}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {loaded_count} products from {fixture_path}'))
