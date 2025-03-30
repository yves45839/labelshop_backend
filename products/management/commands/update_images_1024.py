from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product

class Command(BaseCommand):
    help = "Met à jour image_1024 à partir des images ajoutées manuellement si aucun lien Odoo ou local n'est spécifié"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for product in products:
            # Seulement si image_1024 n'est pas définie ou est une URL Odoo
            if not product.image_1024 or "odoo.com" in product.image_1024:
                first_image = product.images.first()
                if first_image and first_image.image:
                    product.image_1024 = settings.MEDIA_URL + first_image.image.name
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f"✅ Image mise à jour pour {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Aucune image locale pour {product.name}"))
            else:
                self.stdout.write(self.style.NOTICE(f"ℹ️ Image déjà définie localement pour {product.name}"))

        self.stdout.write(self.style.SUCCESS("🎉 Mise à jour des images terminée !"))
