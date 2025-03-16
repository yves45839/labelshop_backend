import xmlrpc.client
import requests
from django.http import JsonResponse
from django.db.models import Q
from .models import Product

# Configuration Odoo
ODOO_URL = "https://labr1.odoo.com"
DB_NAME = "labr1"
UID = 2  # Remplace par ton UID Odoo
API_KEY = "08236cb28addcd5d40fa07e43eeabace4e1a4ffd"

# 🔹 1️⃣ Récupération des produits depuis Odoo et stockage en base
def fetch_odoo_products(request):
    try:
        # Connexion XML-RPC à Odoo
        url = f"{ODOO_URL}/xmlrpc/2/object"
        client = xmlrpc.client.ServerProxy(url)

        # Récupérer les produits avec les champs optimisés
        products = client.execute_kw(
            DB_NAME, UID, API_KEY,
            "product.product", "search_read",
            [[]],  # Aucun filtre, récupère tous les produits
            {
                "fields": [
                    "id", "name", "list_price", "default_code", "barcode",
                    "categ_id", "image_1920", "image_1024", "image_512", "image_256",
                    "description", "standard_price", "website_published", "qty_available"
                ],
                "limit": 5000  #
            }
        )

        if not products:
            return JsonResponse({"message": "Aucun produit trouvé dans Odoo"}, status=404)

        # Enregistrement des produits dans la base Django
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
                    "stock_quantity": prod.get("qty_available", 0),  # Stock disponible
                    "rating": prod.get("rating", 0),
                    "is_available": prod.get("website_published", False),
                    "meta_title": prod.get("meta_title", ""),
                    "meta_description": prod.get("meta_description", ""),
                    "search_tags": prod.get("search_tags", ""),
                }
            )

        return JsonResponse({"message": f"{len(products)} produits mis à jour."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# 🔹 2️⃣ Recherche avancée de produits (SEO + Optimisation)
def search_products(request):
    query = request.GET.get('q', '')

    # Première tentative : Recherche exacte sur le slug
    product = Product.objects.filter(slug=query).first()

    # Deuxième tentative : Recherche partielle si aucun résultat exact
    if not product:
        product = Product.objects.filter(slug__icontains=query).first()

    # Si le produit existe, retourner les données, sinon tableau vide
    if product:
        return JsonResponse([{
            "id": product.id,
            "odoo_id": product.odoo_id,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "short_description": product.short_description,
            "list_price": product.list_price,
            "discount_price": product.discount_price,
            "stock_quantity": product.stock_quantity,
            "is_available": product.is_available,
            "default_code": product.default_code,
            "barcode": product.barcode,
            "categ_id": product.categ_id,
            "brand": product.brand,
            "rating": product.rating,
            "reviews_count": product.reviews_count,
            "image_url": product.image_url,
            "image_1920": product.image_1920,
            "image_1024": product.image_1024,
            "image_512": product.image_512,
            "image_256": product.image_256,
            "meta_title": product.meta_title,
            "meta_description": product.meta_description,
            "keywords": product.keywords,
            "search_tags": product.search_tags,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }], safe=False)

    return JsonResponse([], safe=False)


# 🔹 3️⃣ Liste des produits stockés en base
def get_products(request):
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)
