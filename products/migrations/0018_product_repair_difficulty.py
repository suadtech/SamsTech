# Generated by Django 5.2.3 on 2025-06-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_product_category_path_product_excludes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='repair_difficulty',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
