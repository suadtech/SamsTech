import json
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Category # Import Product and Category models

class Command(BaseCommand):
    help = 'Loads SamTech products from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing product data.')
        parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without saving to the database.')
        parser.add_argument('--clear-existing', action='store_true', help='Clear all existing products before loading new ones.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('✨ SamTech Product Loader'))

        json_file_path = options['json_file']
        dry_run = options['dry_run']
        clear_existing = options['clear_existing']

        if dry_run:
            self.stdout.write(self.style.WARNING('Performing a DRY RUN. No changes will be saved to the database.'))

        if clear_existing:
            if not dry_run:
                self.stdout.write(self.style.WARNING('Clearing all existing products...'))
                Product.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Existing products cleared.'))
            else:
                self.stdout.write(self.style.WARNING('DRY RUN: Would clear all existing products.'))

        try:
            with open(json_file_path, 'r') as f:
                all_data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Error: JSON file not found at "{json_file_path}"')
        except json.JSONDecodeError:
            raise CommandError(f'Error: Could not decode JSON from "{json_file_path}". Please check the file format.')

        # Filter for product models only
        products_data = [item for item in all_data if item.get('model') == 'products.product']

        if not products_data:
            self.stdout.write(self.style.WARNING('No product data found in the JSON file.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(products_data)} product entries to process.'))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for item in products_data:
            fields = item.get('fields', {})
            pk = item.get('pk') # Get the primary key from the JSON

            # Extract fields, handling potential missing keys or complex structures
            sku = fields.get('sku')
            name = fields.get('name')
            description = fields.get('description')
            price = fields.get('price')
            category_name = fields.get('category') # This is the string name
            rating = fields.get('rating')
            image_url = fields.get('image_url')
            image = fields.get('image')
            brand = fields.get('brand')
            shipping = fields.get('shipping')
            estimated_delivery = fields.get('estimated_delivery')
            vat_status = fields.get('vat_status')
            stock_status = fields.get('stock_status')
            warranty = fields.get('warranty')
            msrp = fields.get('msrp')

            if not sku or not name or price is None or category_name is None:
                self.stdout.write(self.style.WARNING(f'Skipping item with missing essential fields (sku, name, price, category): {item}'))
                skipped_count += 1
                continue

            # Handle complex price structure if it's a dict (e.g., for batteries)
            if isinstance(price, dict):
                price = price.get('single', 0.0) # Take the 'single' price, default to 0.0

            # Convert rating to float if it's a string
            if isinstance(rating, str) and rating.replace('.', '', 1).isdigit():
                rating = float(rating)
            elif rating is None:
                rating = 0.0 # Default rating if none provided

            # Ensure category exists in the database (important for integrity, though Product.category is CharField)
            # This step is more for validation/info, as Product.category is a CharField
            # If Product.category were a ForeignKey, we'd fetch the Category object here.
            if category_name:
                try:
                    Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Category "{category_name}" for product "{name}" (SKU: {sku}) does not exist in Category model. Product will still be loaded with this category name.'))
            
            # Prepare data for update_or_create
            product_data = {
                'sku': sku,
                'name': name,
                'description': description,
                'price': price,
                'category': category_name, # Store the string name
                'rating': rating,
                'image_url': image_url,
                'image': image,
                'brand': brand,
                'shipping': shipping,
                'estimated_delivery': estimated_delivery,
                'vat_status': vat_status,
                'stock_status': stock_status,
                'warranty': warranty,
                'msrp': msrp,
                # Add 'created_at' if it's in your JSON and Product model
                # 'created_at': fields.get('created_at'),
            }

            # Remove None values to avoid overwriting defaults or non-nullable fields unnecessarily
            product_data = {k: v for k, v in product_data.items() if v is not None}

            if not dry_run:
                try:
                    # Use sku as the unique identifier for products
                    product, created = Product.objects.update_or_create(
                        sku=sku,
                        defaults=product_data
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {name} (SKU: {sku})'))
                        created_count += 1
                    else:
                        self.stdout.write(self.style.INFO(f'🔄 Updated: {name} (SKU: {sku})'))
                        updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error processing product "{name}" (SKU: {sku}): {e}'))
                    skipped_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'🔍 DRY RUN: Would process product: {name} (SKU: {sku})'))

        self.stdout.write(self.style.SUCCESS(f'\n--- Product Loading Complete ---'))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped/Errors: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS('✅ Done!'))
