import re


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
