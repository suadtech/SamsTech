# Generated by Django 5.2.3 on 2025-06-29 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_merge_20250629_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
