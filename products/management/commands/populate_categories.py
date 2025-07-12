# products/management/commands/populate_categories.py

from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Populates the Category model from the unique categories in the Product model'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate categories...')
        
        # Get all unique category names from the Product model
        unique_category_names = Product.objects.values_list('category', flat=True).distinct()
        
        created_count = 0
        for name in unique_category_names:
            if name:  # Ensure the name is not an empty string
                # get_or_create is safe. It won't create duplicates.
                category, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'friendly_name': name} # Use the name as the friendly_name by default
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Finished. Created {created_count} new categories.'))
