import csv
import base64
import os
import re

csv.field_size_limit(2147483647)  # Corrige la limite du CSV

csv_path = r"C:\Users\HP ELITEBOOK 840 G3\Downloads\Variante de produit (product.product).csv"
output_dir = os.path.join("..", "..", "..", "media", "products")

os.makedirs(output_dir, exist_ok=True)

def clean_filename(name):
    """ Enlever les caractères interdits dans les noms de fichiers """
    return re.sub(r'[\\/*?:"<>|]', "_", name)

with open(csv_path, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        barcode = row.get('Code-barres', '').strip()
        image_base64 = row.get('Image 1024', '').strip()

        if barcode and image_base64:
            try:
                image_data = base64.b64decode(image_base64)
                safe_barcode = clean_filename(barcode)  # Nettoyage du nom de fichier
                image_path = os.path.join(output_dir, f"{safe_barcode}.jpeg")
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
                print(f"✅ Image sauvegardée : {safe_barcode}.jpeg")
            except Exception as e:
                print(f"Erreur décodage image {barcode} : {e}")
        else:
            print(f"Ligne ignorée (barcode/image manquante) : {row.get('Nom', 'Inconnu')}")

print("🎉 Terminé !")
