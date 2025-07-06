from django.core.management.base import BaseCommand
from products.models import Product
from products.classifier import classify

class Command(BaseCommand):
    help = "Applique la fonction classify à tous les produits pour renseigner categ_id"

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.all():
            sku = product.default_code or product.name
            category = " / ".join(classify(sku))
            if product.categ_id != category:
                product.categ_id = category
                product.save(update_fields=["categ_id"])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"{updated} produits mis à jour"))
