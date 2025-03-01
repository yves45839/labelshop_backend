from django.core.management.base import BaseCommand
from products.utils import fetch_products_from_odoo

class Command(BaseCommand):
    help = "Importe les produits depuis Odoo"

    def handle(self, *args, **kwargs):
        fetch_products_from_odoo()
        self.stdout.write(self.style.SUCCESS("Produits importés avec succès !"))
