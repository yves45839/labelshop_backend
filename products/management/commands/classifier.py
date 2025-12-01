import re
from typing import Optional, Tuple

from django.core.management.base import BaseCommand
from products.models import Product

# ------------------------------------------------------------------ #
#   REGLES HIKVISION (famille, categorie, type)                      #
# ------------------------------------------------------------------ #

HIK_RULES: list[Tuple[str, Tuple[str, str, Optional[str]]]] = [
    # 1. Interphonie & controle d'acces
    (r"^I?DS-K1T", ("Controle d'acces", "Terminaux autonomes", "Terminal autonome")),
    (r"^I?DS-K1A", ("Controle d'acces", "Temps de presence", "Terminal de pointage")),
    (r"^I?DS-K2", ("Controle d'acces", "Controleurs & modules", "Controleur de porte")),
    (r"^I?DS-K3", ("Controle d'acces", "Portillons & tourniquets", None)),
    (r"^I?DS-K4", ("Controle d'acces", "Serrures & ventouses", None)),
    (r"^I?DS-KAS", ("Controle d'acces", "Kits & accessoires", None)),

    (r"^I?DS-KH", ("Interphonie", "Moniteurs interieurs", "Moniteur interieur")),
    (r"^I?DS-KV", ("Interphonie", "Platines de rue & doorbells", "Platine de rue villa")),
    (r"^I?DS-KD", ("Interphonie", "Platines de rue & doorbells", "Platine modulaire")),
    (r"^I?DS-KB", ("Interphonie", "Platines de rue & doorbells", "Sonnette video")),
    (r"^I?DS-KIS", ("Interphonie", "Kits video", None)),

    # 2. Alarmes intrusion
    (r"^I?DS-PWA", ("Alarme intrusion", "Centrales", "Centrale AX PRO")),
    (r"^I?DS-PD", ("Alarme intrusion", "Detecteurs / contacts / sirenes", "Detecteur / contact")),
    (r"^I?DS-PS", ("Alarme intrusion", "Detecteurs / contacts / sirenes", "Sirene")),
    (r"^I?DS-PM", ("Alarme intrusion", "Peripheriques", "Module / expander")),
    (r"^I?DS-P", ("Alarme intrusion", "AX PRO & peripheriques", None)),

    # 3. Video - cameras
    (r"^I?DS-2CD63", ("Videosurveillance IP", "Cameras IP", "Camera fisheye IP")),
    (r"^I?DS-2DP", ("Videosurveillance IP", "Cameras panoramiques", "PanoVu")),
    (r"^I?DS-2CD", ("Videosurveillance IP", "Cameras IP", "Camera IP fixe")),
    (r"^I?DS-2CV", ("Videosurveillance IP", "Cameras IP", "Camera IP Wi-Fi")),
    (r"^I?DS-2XS", ("Videosurveillance IP", "Cameras IP", "Camera IP solaire")),
    (r"^(I?DS-2CE|DS-2CS|DS-2CC)", ("Videosurveillance analogique", "Cameras analogiques", "Camera TurboHD")),
    (r"^I?DS-2DF", ("Videosurveillance IP", "Cameras PTZ", "Camera PTZ IP")),
    (r"^I?DS-2DE", ("Videosurveillance IP", "Cameras PTZ", "Camera PTZ IP")),
    (r"^I?DS-2AE", ("Videosurveillance analogique", "Cameras PTZ", "Camera PTZ analogique")),
    (r"^I?DS-2TD", ("Videosurveillance specialisee", "Cameras thermiques", "Camera thermique")),
    (r"^I?DS-2TP", ("Videosurveillance specialisee", "Cameras thermiques", "Camera thermique portative")),
    (r"^I?DS-2TR", ("Videosurveillance specialisee", "Cameras thermiques", "Lunette / scope thermique")),
    (r"^I?DS-2", ("Videosurveillance IP", "Cameras IP", "Camera IP fixe")),  # fallback Hikvision DS-2..
    (r"^CS-", ("Videosurveillance IP", "Cameras IP", None)),

    # 4. Video - enregistreurs
    (r"^I?DS-7\d{2}(HGHI|HQHI|HUHI|HTHI)", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^I?DS-71\d{2}(HGHI|HQHI|HUHI|HTHI)", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^I?DS-72", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^I?DS-73", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^I?DS-81", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^I?DS-90", ("Enregistreurs", "DVR analogiques", "DVR hybride")),
    (r"^I?DS-7(1|6|7|9)\d{2}N(XI)?", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^I?DS-76", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^I?DS-77", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^I?DS-86", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^I?DS-96", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-E.*(HGHI|HQHI)", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),
    (r"^DS-E.*NI", ("Enregistreurs", "NVR IP", "NVR IP")),
    (r"^DS-J\d+.*HGHI", ("Enregistreurs", "DVR analogiques", "DVR Turbo HD")),

    # 5. Reseau / affichage / stockage
    (r"^DS-3E", ("Reseau & transmission", "Switches PoE", "Switch reseau")),
    (r"^DS-3T", ("Reseau & transmission", "Switches PoE", "Switch reseau")),
    (r"^DS-3W", ("Reseau & transmission", "Equipements reseau", None)),
    (r"^DS-69", ("Affichage & mur d'images", "Decoders / controleurs mur", None)),
    (r"^DS-D", ("Affichage & mur d'images", "Moniteurs / video-wall / LED", None)),
    (r"^DS-A7", ("Stockage", "Serveurs de stockage", "Hybrid SAN / iSCSI")),
    (r"^DS-A8", ("Stockage", "Serveurs de stockage", "Hybrid SAN / iSCSI")),
    (r"^HS-A", ("Stockage", "Serveurs de stockage", "NAS / stockage IP")),
    (r"^DS-UPS", ("Accessoires generaux", "Alimentation & UPS", "Onduleur")),

    # Cables / supports
    (r"^DS-1L", ("Reseau & transmission", "Cables reseau", "Cable UTP/FTP")),
    (r"^DS-1", ("Accessoires", "Cables & transmission", None)),
    (r"^DS-12", ("Accessoires", "Supports & boitiers", None)),
    (r"^DS-13", ("Accessoires", "Supports & boitiers", None)),
    (r"^DSK4", ("Controle d'acces", "Serrures & ventouses", None)),

    # 6. Trafic / parking
    (r"^DS-TMG", ("Trafic / Parking", "Gestion d'acces vehicules", "Radar entree/sortie")),
    (r"^DS-TCG", ("Trafic / Parking", "Reconnaissance de plaques", "Camera ANPR")),

    # 7. Accessoires generaux (HDD, connectique…)
    (r"^CAT *6", ("Accessoires generaux", "Cables & connectique", "Cable reseau CAT6")),
    (r"^CAT *7", ("Accessoires generaux", "Cables & connectique", "Cable reseau CAT7")),
    (r".*CAT *6", ("Accessoires generaux", "Cables & connectique", "Cable reseau CAT6")),
    (r".*CAT *7", ("Accessoires generaux", "Cables & connectique", "Cable reseau CAT7")),
    (r"RG59|RJ59", ("Accessoires generaux", "Cables & connectique", None)),
    (r"COXIAL|COAXIAL", ("Accessoires generaux", "Cables & connectique", None)),
    (r"^EV-CA", ("Accessoires generaux", "Cables & connectique", None)),
    (r"^NC634", ("Accessoires generaux", "Cables & connectique", "Cable reseau CAT6")),
    (r"^COFFRET", ("Accessoires generaux", "Supports & boitiers", None)),
    (r"^EXTENDER", ("Accessoires generaux", "Accessoires divers", None)),
    (r"GACHE", ("Accessoires generaux", "Accessoires divers", None)),
    (r"GTECH", ("Accessoires generaux", "Cables & connectique", None)),
    (r"MICRO", ("Accessoires generaux", "Accessoires divers", None)),
    (r"^LKV", ("Accessoires generaux", "Accessoires divers", None)),
    (r"^HDD", ("Stockage", "Disques durs", None)),
    (r"^DISQUEDUR", ("Stockage", "Disques durs", None)),
    (r"^ST\d+VX", ("Stockage", "Disques durs", None)),
    (r"^(3TO|4TO|6TERA|1TO|2TO|500GO)", ("Stockage", "Disques durs", "HDD videosurveillance")),
    (r"^(BNC|DC|RCA)", ("Accessoires generaux", "Cables & connectique", "Connecteurs & fiches")),
    (r"CONNECTEUR", ("Accessoires generaux", "Cables & connectique", None)),
    (r"CONNECTEURS", ("Accessoires generaux", "Cables & connectique", None)),
    (r"CG577", ("Accessoires generaux", "Cables & connectique", None)),
    (r"^DS-KP", ("Interphonie", "Accessoires", None)),
    (r"^NK\d+", ("Enregistreurs", "NVR IP", "Kit NVR IP")),
    (r"^OUTDOOR.*FTP", ("Accessoires generaux", "Cables & connectique", "Cable reseau")),
    (r"^HF-S", ("Accessoires generaux", "Accessoires divers", None)),
    (r"^IC ?S50", ("Accessoires generaux", "Badges & cartes", None)),
    (r"^S50\+TK4100", ("Controle d'acces", "Badges & cartes", "Carte RFID/MIFARE")),
    (r"^NP-SH", ("Accessoires generaux", "Accessoires divers", None)),
    (r"^DS-H", ("Accessoires generaux", "Accessoires divers", None)),
]


def infer_categories(
    default_code: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Retourne (famille, categorie, type) pour une reference Hikvision."""
    if not default_code:
        return existing_main, existing_sub, None

    normalized_code = str(default_code).strip().upper().replace(" ", "")
    if normalized_code in {"FALSE", "NONE"}:
        return existing_main, existing_sub, None

    for pattern, (main, sub, type_) in HIK_RULES:
        if re.match(pattern, normalized_code):
            return main, sub, type_

    return existing_main, existing_sub, None


def classify(
    sku_raw: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
):
    """Retourne une liste [famille, categorie, type] pour un SKU donne."""
    main, sub, type_ = infer_categories(sku_raw, existing_main, existing_sub)

    if not main and not sub:
        return ["Non classe"]

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
            help="Affiche les resultats sans sauvegarder en base",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        qs = Product.objects.all()
        self.stdout.write(f"Nombre de produits : {qs.count()}")

        updated = 0
        skipped_no_ref = 0
        no_match = 0
        unchanged = 0

        for product in qs:
            ref_raw = (
                getattr(product, "default_code", None)
                or getattr(product, "sku", None)
                or getattr(product, "barcode", None)
                or getattr(product, "slug", None)
                or getattr(product, "name", None)
                or ""
            )
            ref = str(ref_raw).strip()
            if not ref or ref.lower() in {"false", "none"}:
                skipped_no_ref += 1
                continue

            existing_main = getattr(product, "category_main", None)
            existing_sub = getattr(product, "category_sub", None)

            def _clean_existing(value: Optional[str]) -> Optional[str]:
                if isinstance(value, str) and "non class" in value.lower():
                    return None
                return value

            existing_main = _clean_existing(existing_main)
            existing_sub = _clean_existing(existing_sub)

            main, sub, type_ = infer_categories(ref, existing_main, existing_sub)
            self.stdout.write(f"{ref} -> {main} / {sub} / {type_}")

            if not main and not sub:
                no_match += 1
                continue

            if dry_run:
                continue

            fields: list[str] = []
            if hasattr(product, "category_main") and getattr(product, "category_main") != main:
                product.category_main = main
                fields.append("category_main")
            if hasattr(product, "category_sub") and getattr(product, "category_sub") != sub:
                product.category_sub = sub
                fields.append("category_sub")
            if hasattr(product, "category_type") and getattr(product, "category_type") != type_:
                product.category_type = type_
                fields.append("category_type")

            if fields:
                product.save(update_fields=fields)
                updated += 1
            else:
                unchanged += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry-run : aucune modification en base."))

        self.stdout.write(
            self.style.SUCCESS(
                f"Termine. MAJ={updated}, inchanges={unchanged}, sans_ref={skipped_no_ref}, non_matches={no_match}."
            )
        )
