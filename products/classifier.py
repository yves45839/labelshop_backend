import re
from typing import Optional, Tuple


HIK_RULES: list[Tuple[str, Tuple[str, str, Optional[str]]]] = [
    (r"^DS-2CD", ("Vidéosurveillance IP", "Caméras IP", "Caméra IP fixe")),
    (r"^DS-2CE", ("Vidéosurveillance analogique", "Caméras analogiques", "Caméra TurboHD")),
    (r"^DS-2DE|^DS-2DF|^DS-2AE", ("Vidéosurveillance IP", "Caméras PTZ", "PTZ IP")),
    (r"^DS-2TD|^DS-2T", ("Vidéosurveillance spécialisée", "Caméras thermiques", "Thermique")),
    (r"^DS-2DP", ("Vidéosurveillance IP", "Caméras multi-capteurs", "PanoVu")),
    (r"^DS-76|^DS-77|^DS-86|^DS-96", ("Enregistreurs", "NVR IP", "NVR")),
    (r"^DS-71|^DS-72|^DS-73|^DS-81|^DS-90", ("Enregistreurs", "DVR analogiques", "DVR")),
    (r"^DS-K1T", ("Contrôle d'accès", "Terminaux autonomes", "Terminal contrôle d'accès")),
    (r"^DS-K1A", ("Contrôle d'accès", "Temps de présence", "Terminal de pointage")),
    (r"^DS-K2", ("Contrôle d'accès", "Contrôleurs & modules", None)),
    (r"^DS-K3", ("Contrôle d'accès", "Portillons & tourniquets", None)),
    (r"^DS-K4", ("Contrôle d'accès", "Serrures & ventouses", None)),
    (r"^DS-KH", ("Interphonie", "Moniteurs intérieurs", None)),
    (r"^DS-KV|^DS-KD|^DS-KB", ("Interphonie", "Platines de rue & doorbells", None)),
    (r"^DS-1L", ("Réseau & transmission", "Câbles réseau", "Câble UTP/FTP")),
    (r"^DS-3E", ("Réseau & transmission", "Switches PoE", "Switch réseau")),
    (r"^DS-P", ("Alarme intrusion", "AX PRO & périphériques", None)),
    (r"^(3TO|4TO|6TERA|1TO|2TO|500GO)", ("Stockage", "Disques durs", "HDD vidéosurveillance")),
    (r"^(BNC|DC|RCA)", ("Accessoires généraux", "Câbles & connectique", "Connecteurs & fiches")),
]


def infer_categories(
    default_code: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Return the most accurate category tuple for a product.

    The classification relies primarily on the product reference (default code) and
    falls back to existing categories when no rule matches.
    """

    if not default_code:
        return existing_main, existing_sub, None

    normalized_code = default_code.strip().upper()

    for pattern, (main, sub, type_) in HIK_RULES:
        if re.match(pattern, normalized_code):
            return main, sub, type_

    return existing_main, existing_sub, None


def classify(
    sku_raw: str,
    existing_main: Optional[str] = None,
    existing_sub: Optional[str] = None,
):
    """Return category path list for a given SKU or label."""

    main, sub, type_ = infer_categories(sku_raw, existing_main, existing_sub)

    if not main and not sub:
        return ["Non classé"]

    return [main, sub, type_]
