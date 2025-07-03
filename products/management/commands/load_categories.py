import json
from django.core.management.base import BaseCommand, CommandError
from products.models import Category 
class Command(BaseCommand):
    help = 'Loads SamTech categories from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file containing category data.')
        parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without saving to the database.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('✨ SamTech Category Loader'))

        json_file_path = options['json_file']
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('Performing a DRY RUN. No changes will be saved to the database.'))

        try:
            with open(json_file_path, 'r') as f:
                all_data = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'Error: JSON file not found at "{json_file_path}"')
        except json.JSONDecodeError:
            raise CommandError(f'Error: Could not decode JSON from "{json_file_path}". Please check the file format.')

        categories_data = [item for item in all_data if item.get('model') == 'products.category']

        if not categories_data:
            self.stdout.write(self.style.WARNING('No category data found in the JSON file.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(categories_data)} category entries to process.'))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for item in categories_data:
            fields = item.get('fields', {})
            category_name = fields.get('name')
            friendly_name = fields.get('friendly_name')

            if not category_name:
                self.stdout.write(self.style.WARNING(f'Skipping item with missing "name" field: {item}'))
                skipped_count += 1
                continue

            if not dry_run:
                try:
                    category, created = Category.objects.update_or_create(
                        name=category_name,
                        defaults={'friendly_name': friendly_name}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {friendly_name} (name: {category_name})'))
                        created_count += 1
                    else:
                        # Changed from self.style.INFO to self.style.NOTICE
                        self.stdout.write(self.style.NOTICE(f'🔄 Updated: {friendly_name} (name: {category_name})'))
                        updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error processing category "{category_name}": {e}'))
                    skipped_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'🔍 DRY RUN: Would process category: {friendly_name} (name: {category_name})'))

        # These summary lines MUST be inside the handle method
        self.stdout.write(self.style.SUCCESS(f'\n--- Loading Complete ---'))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.NOTICE(f'Updated: {updated_count}')) # Changed to NOTICE
        self.stdout.write(self.style.WARNING(f'Skipped/Errors: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS('✅ Done!'))



