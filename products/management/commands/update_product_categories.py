from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Create SamTech categories'

    def add_arguments(self, parser):
        parser.add_argument('--create-sample', action='store_true')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        self.stdout.write('�� SamTech Category Creator')
        
        if options['create_sample']:
            self.create_categories(options['dry_run'])
        
        self.stdout.write('✅ Done!')

    def create_categories(self, dry_run=False):
        categories = [
        ]
        for name, friendly_name in categories:
            if not dry_run:
                category, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'friendly_name': friendly_name}
                )
                if created:
                    self.stdout.write(f'✅ Created: {friendly_name}')
                else:
                    self.stdout.write(f'🔄 Exists: {friendly_name}')
            else:
                self.stdout.write(f'🔍 DRY RUN: {friendly_name}')
