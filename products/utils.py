import xmlrpc.client
from .models import Product
from django.utils.text import slugify
from .classifier import classify


ODOO_URL = "https://labr1.odoo.com/xmlrpc/2/object"
DB_NAME = "labr1"
UID = 2  # Remplace par ton UID correct
API_KEY = "08236cb28addcd5d40fa07e43eeabace4e1a4ffd"


def _extract_odoo_categories(categ_label: str):
    """Split an Odoo category label into main and sub categories."""

    if not categ_label:
        return None, None

    parts = [part.strip() for part in categ_label.split("/") if part.strip()]
    if not parts:
        return None, None

    if len(parts) == 1:
        return parts[0], None

    return parts[0], " / ".join(parts[1:])

def fetch_products_from_odoo():
    client = xmlrpc.client.ServerProxy(ODOO_URL)

    products = client.execute_kw(
        DB_NAME, UID, API_KEY,
        'product.product', 'search_read',
        [[]],
        {
            'fields': [
                'id', 'name', 'description_sale', 'list_price', 'default_code', 'barcode',
                'categ_id', 'image_1920', 'image_1024', 'image_512', 'image_256',
                'standard_price', 'qty_available'
            ]
        }
    )

    for product in products:
        existing_main, existing_sub = _extract_odoo_categories(product['categ_id'][1]) if product.get('categ_id') else (None, None)
        categories = classify(
            product.get('default_code') or product.get('barcode') or product['name'],
            existing_main,
            existing_sub,
        )

        Product.objects.update_or_create(
            odoo_id=product['id'],
            defaults={
                'name': product['name'],
                'slug': slugify(product['name']),
                'description': product.get('description_sale', ''),
                'short_description': product.get('description_sale', '')[:150],  # Extrait de 150 caractères
                'list_price': product['list_price'],
                'discount_price': product.get('standard_price', None),
                'stock_quantity': product.get('qty_available', 0),
                'is_available': product.get('qty_available', 0) > 0,
                'default_code': product.get('default_code', ''),
                'barcode': product.get('barcode', ''),
                'categ_id': product['categ_id'][1] if product.get('categ_id') else 'Inconnu',
                'image_url': f"https://labr1.odoo.com/web/image/product.product/{product['id']}/image_1024",
                'image_1920': f"https://labr1.odoo.com/web/image/product.product/{product['id']}/image_1920",
                'image_1024': f"https://labr1.odoo.com/web/image/product.product/{product['id']}/image_1024",
                'image_512': f"https://labr1.odoo.com/web/image/product.product/{product['id']}/image_512",
                'image_256': f"https://labr1.odoo.com/web/image/product.product/{product['id']}/image_256",
                'meta_title': f"{product['name']} | Label Retail",
                'meta_description': f"Achetez {product['name']} au meilleur prix sur Label Retail. Livraison rapide et garantie de qualité.",
                'keywords': f"{product['name']}, {product['categ_id'][1] if product.get('categ_id') else ''}, sécurité, électricité, vidéosurveillance",
                'search_tags': f"{product['name']}, {product['default_code']}, {product.get('barcode', '')}",
                'category_main': categories[0] if len(categories) > 0 else None,
                'category_sub': categories[1] if len(categories) > 1 else None,
                'category_type': categories[2] if len(categories) > 2 else None,
            }
        )
