from django.db import migrations
from products.classifier import classify


def populate_categories(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        categories = classify(product.barcode or product.default_code or product.name)
        product.category_main = categories[0] if len(categories) > 0 else None
        product.category_sub = categories[1] if len(categories) > 1 else None
        product.category_type = categories[2] if len(categories) > 2 else None
        product.save(update_fields=['category_main', 'category_sub', 'category_type'])

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_categories'),
    ]

    operations = [
        migrations.RunPython(populate_categories, migrations.RunPython.noop),
    ]
