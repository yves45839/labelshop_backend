from decimal import Decimal, ROUND_HALF_UP

from django.db import migrations


def increase_product_prices(apps, schema_editor):
    Product = apps.get_model("products", "Product")

    for product in Product.objects.all().iterator():
        current_price = Decimal(str(product.list_price))
        product.list_price = float(
            (current_price * Decimal("1.20")).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        )
        product.save(update_fields=["list_price"])


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_populate_product_categories"),
    ]

    operations = [
        migrations.RunPython(
            increase_product_prices,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
