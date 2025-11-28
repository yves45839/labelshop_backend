import re
from typing import Optional, Tuple

from django.core.management.base import BaseCommand
from products.models import Product  # adapte si ton modèle est ailleurs

# ------------------------------------------------------------------ #
#   RÈGLES HIKVISION (famille, catégorie, type)                      #
# ------------------------------------------------------------------ #

HIK_RULES: list[Tuple[str, Tuple[str, str, Optional[str]]]] = [
    # 1. Interphonie & contrôle d’accès
    (r"^I?DS-K1T", ("Contrôle d'accès", "Terminaux autonomes", "Terminal autonome")),
    (r"^I?DS-K1A", ("Contrôle d'accès", "Temps de présence", "Terminal de pointage")),
    (r"^I?DS-K2",  ("Contrôle d'accès", "Contrôleurs & modules", "Contrôleur de porte")),
    (r"^I?DS-K3",  ("Contrôle d'accès", "Portillons & tourniquets", None)),
    (r"^I?DS-K4",  ("Contrôle d'accès", "Serrures & ventouses", None)),

    (r"^I?DS-KH", ("Interphonie", "Moniteurs intérieurs", "Moniteur intérieur")),
    (r"^I?DS-KV", ("Interphonie", "Platines de rue & doorbells", "Platine de rue villa")),
    (r"^I?DS-KD", ("Interphonie", "Platines de rue & doorbells", "Platine modulaire")),
    (r"^I?DS-KB", ("Interphonie", "Platines de rue & doorbells", "Sonnette vidéo")),

    # 2. Alarmes intrusion
    (r"^I?DS-PWA", ("Alarme intrusion", "Centrales", "Centrale AX PRO")),
    (r"^I?DS-PD",  ("Alarme intrusion", "Détecteurs / contacts / sirènes", "Détecteur / contact")),
    (r"^I?DS-PS",  ("Alarme intrusion", "Détecteurs / contacts / sirènes", "Sirène")),
    (r"^I?DS-PM",  ("Alarme intrusion", "Périphériques", "Module / expander")),
    (r"^I?DS-P",   ("Alarme intrusion", "AX PRO & périphériques", None)),

    # 3. Vidéo – caméras
    (r"^I?DS-2CD63", ("Vidéosurveillance IP", "Caméras IP", "Caméra fisheye IP")),
    (r"^I?DS-2DP",   ("Vidéosurveillance IP", "Caméras panoramiques", "PanoVu")),

    (r"^I?DS-2CD", ("Vidéosurveillance IP", "Caméras IP", "Caméra IP fixe")),
    (r"^I?DS-2CV", ("Vidéosurveillance IP", "Caméras IP", "Caméra IP Wi-Fi")),
    (r"^I?DS-2XS", ("Vidéosurveillance IP", "Caméras IP", "Caméra IP solaire")),

    (r"^(I?DS-2CE|DS-2CS|DS-2CC)", ("Vidéosurveillance analogique", "Caméras analogiques", "Caméra TurboHD")),

    (r"^I?DS-2DF", ("Vidéosurveillance IP", "Caméras PTZ", "Caméra PTZ IP")),
    (r"^I?DS-2DE", ("Vidéosurveillance IP", "Caméras PTZ", "Caméra PTZ IP")),
    (r"^I?DS-2AE", ("Vidéosurveillance analogique", "Caméras PTZ", "Caméra PTZ analogique")),

    (r"^I?DS-2TD", ("Vidéosurveillance spécialisée", "Caméras thermiques", "Caméra thermique")),
    (r"^I?DS-2TP", ("Vidéosurveillance spécialisée", "Caméras thermiques", "Caméra thermique portative")),
    (r"^I?DS-2TR", ("Vidéosurveillance spécialisée", "Caméras thermiques", "Lunette / scope thermique")),

    # 4. Vidéo – enregistreurs
    (r"^DS-7\d{2}(HGHI|HQHI|HUHI|HTHI)", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-71\d{2}(HGHI|HQHI|HUHI|HTHI)", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-72", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-73", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-81", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-90", ("Enregistreurs", "DVR analogiques", "DVR hybride")),

    (r"^DS-7(1|6|7|9)\d{2}N(XI)?", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-76", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-77", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-86", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-96", ("Enregistreurs", "NVR IP", "NVR IP")),

    # 5. Réseau / affichage / stockage
    (r"^DS-3E", ("Réseau & transmission", "Switches PoE", "Switch réseau")),
    (r"^DS-D",  ("Affichage & mur d’images", "Moniteurs / vidéo-wall / LED", None)),

    (r"^DS-A7", ("Stockage", "Serveurs de stockage", "Hybrid SAN / iSCSI")),
    (r"^DS-A8", ("Stockage", "Serveurs de stockage", "Hybrid SAN / iSCSI")),
    (r"^HS-A",  ("Stockage", "Serveurs de stockage", "NAS / stockage IP")),

    (r"^DS-1[0-9]", ("Accessoires", "Câbles & transmission", None)),
    (r"^DS-12",    ("Accessoires", "Supports & boîtiers", None)),
    (r"^DS-13",    ("Accessoires", "Supports & boîtiers", None)),

    # 6. Trafic / parking
    (r"^DS-TMG", ("Trafic / Parking", "Gestion d’accès véhicules", "Radar entrée/sortie")),
    (r"^DS-TCG", ("Trafic / Parking", "Reconnaissance de plaques", "Caméra ANPR")),

    # 7. Accessoires généraux (HDD, connectique…)
    (r"^(3TO|4TO|6TERA|1TO|2TO|500GO)", ("Stockage", "Disques durs", "HDD vidéosurveillance")),
    (r"^(BNC|DC|RCA)", ("Accessoires généraux", "Câbles & connectique", "Connecteurs & fiches")),
]


def infer_categories(
    default_code: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Retourne (famille, catégorie, type) pour une référence Hikvision.
    """
    if not default_code:
        return existing_main, existing_sub, None

    normalized_code = default_code.strip().upper().replace(" ", "")

    for pattern, (main, sub, type_) in HIK_RULES:
        if re.match(pattern, normalized_code):
            return main, sub, type_

    return existing_main, existing_sub, None


def classify(
    sku_raw: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
):
    """
    Retourne une liste [famille, catégorie, type] pour un SKU donné.
    """
    main, sub, type_ = infer_categories(sku_raw, existing_main, existing_sub)

    if not main and not sub:
        return ["Non classé"]

    return [main, sub, type_]


# ------------------------------------------------------------------ #
#   COMMANDE DJANGO                                                  #
# ------------------------------------------------------------------ #

class Command(BaseCommand):
    help = "Applique la classification Hikvision aux produits"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Affiche les résultats sans sauvegarder en base",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        # tu peux filtrer sur la marque si tu veux :
        qs = Product.objects.all()
        # qs = Product.objects.filter(brand__name__icontains="hikvision")

        self.stdout.write(f"Nombre de produits : {qs.count()}")

        for product in qs:
            ref = (getattr(product, "default_code", "") or getattr(product, "sku", "") or "").strip()
            if not ref:
                continue

            # on suppose que ton modèle a ces champs :
            existing_main = getattr(product, "category_main", None)
            existing_sub = getattr(product, "category_sub", None)

            main, sub, type_ = infer_categories(ref, existing_main, existing_sub)

            self.stdout.write(f"{ref} -> {main} / {sub} / {type_}")

            if not dry_run:
                if hasattr(product, "category_main"):
                    product.category_main = main
                if hasattr(product, "category_sub"):
                    product.category_sub = sub
                if hasattr(product, "category_type"):
                    product.category_type = type_

                fields = []
                if hasattr(product, "category_main"):
                    fields.append("category_main")
                if hasattr(product, "category_sub"):
                    fields.append("category_sub")
                if hasattr(product, "category_type"):
                    fields.append("category_type")

                if fields:
                    product.save(update_fields=fields)
