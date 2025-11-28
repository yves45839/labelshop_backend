from django.core.management.base import BaseCommand
from products.models import Product
from products.classifier import classify

class Command(BaseCommand):
    help = "Classifie les produits en fonction de leur référence SKU"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        updated = 0

        for product in products:
            code = product.barcode or product.default_code or product.name
            result = classify(code)

            if hasattr(product, "category_main"):
                product.category_main = result[0]
            if len(result) > 1 and hasattr(product, "category_sub"):
                product.category_sub = result[1]
            if len(result) > 2 and hasattr(product, "category_type"):
                product.category_type = result[2]

            product.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"{updated} produits mis à jour avec classification."))
