import xmlrpc.client
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from urllib.parse import urljoin
from django.conf import settings
from .models import Product

# Configuration Odoo
ODOO_URL = "https://labr1.odoo.com"
DB_NAME = "labr1"
UID = 2  # Remplace par ton UID Odoo
API_KEY = "08236cb28addcd5d40fa07e43eeabace4e1a4ffd"

def build_absolute_url(request, url):
    if url.startswith('http'):
        return url
    return request.build_absolute_uri(urljoin(settings.MEDIA_URL, url.lstrip('/')))

# 🔹 1️⃣ Récupération des produits depuis Odoo et stockage en base
def fetch_odoo_products(request):
    try:
        url = f"{ODOO_URL}/xmlrpc/2/object"
        client = xmlrpc.client.ServerProxy(url)

        products = client.execute_kw(
            DB_NAME, UID, API_KEY,
            "product.product", "search_read",
            [[]],
            {
                "fields": [
                    "id", "name", "list_price", "default_code", "barcode",
                    "categ_id", "image_1920", "image_1024", "image_512", "image_256",
                    "description", "standard_price", "website_published", "qty_available"
                ],
                "limit": 5000
            }
        )

        if not products:
            return JsonResponse({"message": "Aucun produit trouvé dans Odoo"}, status=404)

        for prod in products:
            Product.objects.update_or_create(
                odoo_id=prod["id"],
                defaults={
                    "name": prod["name"],
                    "list_price": prod.get("list_price", 0),
                    "default_code": prod.get("default_code", ""),
                    "barcode": prod.get("barcode", ""),
                    "categ_id": prod["categ_id"][1] if prod["categ_id"] else "Non classé",
                    "image_1920": f"{ODOO_URL}/web/image/product.product/{prod['id']}/image_1920" if prod.get("image_1920") else None,
                    "image_1024": f"{ODOO_URL}/web/image/product.product/{prod['id']}/image_1024" if prod.get("image_1024") else None,
                    "image_512": f"{ODOO_URL}/web/image/product.product/{prod['id']}/image_512" if prod.get("image_512") else None,
                    "image_256": f"{ODOO_URL}/web/image/product.product/{prod['id']}/image_256" if prod.get("image_256") else None,
                    "description": prod.get("description", ""),
                    "stock_quantity": prod.get("qty_available", 0),
                    "is_available": prod.get("website_published", False)
                }
            )

        return JsonResponse({"message": f"{len(products)} produits mis à jour."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 🔹 2️⃣ Recherche avancée de produits (SEO + Optimisation)
def search_products(request):
    query = request.GET.get('q', '')
    product = Product.objects.filter(Q(slug=query) | Q(slug__icontains=query)).first()

    if product:
        product_dict = model_to_dict(product)
        for image_field in ['image_1920', 'image_1024', 'image_512', 'image_256']:
            url = getattr(product, image_field, None)
            product_dict[image_field] = build_absolute_url(request, url) if url else None

        return JsonResponse([product_dict], safe=False)

    return JsonResponse([], safe=False)


# 🔹 3️⃣ Liste des produits stockés en base
def get_products(request):
    products = []
    for prod in Product.objects.all():
        prod_dict = model_to_dict(prod)
        for image_field in ['image_1920', 'image_1024', 'image_512', 'image_256']:
            url = getattr(prod, image_field, None)
            prod_dict[image_field] = build_absolute_url(request, url) if url else None

        products.append(prod_dict)

    return JsonResponse(products, safe=False)
