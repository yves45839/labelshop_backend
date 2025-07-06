import xmlrpc.client
import re
from .models import Product
from django.utils.text import slugify


ODOO_URL = "https://labr1.odoo.com/xmlrpc/2/object"
DB_NAME = "labr1"
UID = 2  # Remplace par ton UID correct
API_KEY = "08236cb28addcd5d40fa07e43eeabace4e1a4ffd"

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
                'search_tags': f"{product['name']}, {product['default_code']}, {product.get('barcode', '')}"
            }
        )


def classify(sku_raw: str):
    """Return category path for a given SKU or label."""
    if not sku_raw:
        return ["Non classé"]

    sku = sku_raw.strip().upper()

    def contains_any(text, keywords):
        return any(word in text for word in keywords)

    # --- Vidéo analogique ---------------------------------
    if sku.startswith("DS-2AE"):
        return ["Vidéo analogique", "Caméras PTZ"]
    if sku.startswith("DS-2CE"):
        return ["Vidéo analogique", "Caméras fixes"]
    if sku.startswith("DS-72") or sku.startswith("DS-71"):
        return ["Vidéo analogique", "DVR"]

    # --- Vidéo IP -----------------------------------------
    if sku.startswith("DS-2DF") or sku.startswith("DS-2DE"):
        return ["Vidéo IP", "Caméras PTZ"]
    if sku.startswith("DS-2CD"):
        return ["Vidéo IP", "Caméras fixes"]
    if re.match(r"^DS-7[6-8]", sku):
        return ["Vidéo IP", "NVR"]
    if sku.startswith("DS-3E"):
        return ["Vidéo IP", "Switches PoE"]
    if sku.startswith("DS-A"):
        return ["Vidéo IP", "Stockage IP SAN/NAS"]

    # --- Hybride ------------------------------------------
    if sku.startswith("DS-90"):
        return ["Hybride/HCVR", "DVR Hybride"]

    # --- Contrôle d'accès & Interphonie -------------------
    if sku.startswith("DS-KD"):
        return ["Contrôle d’accès & Interphonie", "Interphonie vidéo", "Door station"]
    if sku.startswith("DS-KH"):
        return ["Contrôle d’accès & Interphonie", "Interphonie vidéo", "Indoor station"]
    if sku.startswith("DS-K1") or sku.startswith("DS-K2"):
        return ["Contrôle d’accès & Interphonie", "Contrôleurs & lecteurs"]

    # --- Alarme intrusion ---------------------------------
    if sku.startswith("DS-PWA") or sku.startswith("DS-PMA"):
        return ["Alarme intrusion", "Centrales"]
    if sku.startswith("DS-PD") or sku.startswith("DS-PS") or sku.startswith("DS-PT") or sku.startswith("DS-PDE"):
        return ["Alarme intrusion", "Détecteurs / contacts / sirènes"]
    if sku.startswith("DS-PK") or sku.startswith("DS-PR") or sku.startswith("DS-PF"):
        return ["Alarme intrusion", "Périphériques"]

    # --- Affichage ----------------------------------------
    if sku.startswith("DS-D5") or sku.startswith("DS-D6"):
        return ["Affichage & mur d’images", "Moniteurs"]
    if sku.startswith("DS-C1") or sku.startswith("DS-VD"):
        return ["Affichage & mur d’images", "Décoders / contrôleurs"]

    # --- Spécialisations diverses -------------------------
    if sku.startswith("DS-M"):
        return ["Autres spécialisations", "Mobile / Bodycam"]
    if sku.startswith("DS-T"):
        return ["Autres spécialisations", "Traffic / radar"]
    if sku.startswith("DS-2TD") or sku.startswith("DS-2TE"):
        return ["Autres spécialisations", "Thermique"]

    # --- Accessoires génériques (mots-clés) ---------------
    if contains_any(sku, ["BALUN", "BNC", "DC", "BRACKET", "MOUNT", "POE", "RJ45"]):
        return ["Accessoires généraux", "Câbles & connectique"]
    if contains_any(sku, ["HDD", "SSD"]):
        return ["Accessoires généraux", "Disques durs"]
    if sku.startswith("DS-12") or sku.startswith("DS-127") or sku.startswith("DS-129"):
        return ["Accessoires généraux", "Supports & boîtiers"]

    # --- Par défaut ---------------------------------------
    return ["Non classé"]
