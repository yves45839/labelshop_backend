import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from products.models import Product
import requests


BROCHURE_BASE_URL = os.environ.get(
    "BROCHURE_BASE_URL",
    "https://example.com/brochures/",
)


class Command(BaseCommand):
    """Download PDF brochures for products and attach them."""

    help = "Télécharge les fiches techniques PDF pour chaque produit."

    def handle(self, *args, **options):
        for product in Product.objects.all():
            if product.pdf_brochure:
                self.stdout.write(
                    self.style.NOTICE(
                        f"ℹ️ Fiche déjà présente pour {product.name}"
                    )
                )
                continue

            identifier = product.barcode or product.default_code
            if not identifier:
                identifier = slugify(product.name)
            pdf_name = f"{identifier}.pdf"
            url = f"{BROCHURE_BASE_URL.rstrip('/')}/{pdf_name}"

            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    product.pdf_brochure.save(
                        pdf_name, ContentFile(response.content), save=True
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Fiche ajoutée pour {product.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️ Fiche manquante pour {product.name}"
                        )
                    )
            except requests.RequestException as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"Erreur téléchargement {product.name}: {exc}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("🎉 Téléchargement terminé"))

