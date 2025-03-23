import os
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings
import re

class Command(BaseCommand):
    help = "Associe automatiquement les images existantes à la propriété image_1024 des produits via leur barcode ou nom."

    def clean_filename(self, name):
        return re.sub(r'[\\/*?:\"<>|]', "_", name)

    def handle(self, *args, **kwargs):
        media_path = os.path.join(settings.MEDIA_ROOT, 'products')
        image_files = {file.lower(): file for file in os.listdir(media_path)}

        for product in Product.objects.all():
            image_filename = None

            if product.barcode:
                safe_barcode = self.clean_filename(product.barcode)
                barcode_filename = f"{safe_barcode}.jpeg"
                if barcode_filename.lower() in image_files:
                    image_filename = image_files[barcode_filename.lower()]

            if not image_filename:
                safe_name = self.clean_filename(product.name)
                name_filename = f"{safe_name}.jpeg"
                if name_filename.lower() in image_files:
                    image_filename = image_files[name_filename.lower()]

            if not image_filename:
                for img_file in image_files:
                    if self.clean_filename(img_file.split('.')[0]) in self.clean_filename(product.name).lower():
                        image_filename = image_files[img_file]
                        break

            if image_filename:
                product.image_1024 = f"/media/products/{image_filename}"
                product.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Image associée pour : {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Aucune image trouvée pour : {product.name}"))

        self.stdout.write(self.style.SUCCESS("🎉 Mise à jour terminée avec succès !"))
