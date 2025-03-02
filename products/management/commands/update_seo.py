from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Met à jour les champs SEO des produits existants"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            product.save()  # Exécute la mise à jour automatique SEO
            print(f"✅ Produit mis à jour : {product.name}")

        self.stdout.write(self.style.SUCCESS(f"🎯 {products.count()} produits mis à jour avec succès !"))
