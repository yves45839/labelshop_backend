from django.test import SimpleTestCase
from products.classifier import classify


class ClassifyTests(SimpleTestCase):
    def test_hikvision_rules(self):
        self.assertEqual(
            classify("DS-2CD2043G2-I"),
            ["Vidéosurveillance IP", "Caméras IP", "Caméra IP fixe"],
        )
        self.assertEqual(
            classify("DS-2DE4425IW-DE"),
            ["Vidéosurveillance IP", "Caméras PTZ", "PTZ IP"],
        )
        self.assertEqual(
            classify("DS-76XXNI"),
            ["Enregistreurs", "NVR IP", "NVR"],
        )
        self.assertEqual(
            classify("DS-K2604"),
            ["Contrôle d'accès", "Contrôleurs & modules", None],
        )
        self.assertEqual(
            classify("BNC-123"),
            ["Accessoires généraux", "Câbles & connectique", "Connecteurs & fiches"],
        )

    def test_fallback_to_existing_categories(self):
        self.assertEqual(
            classify("UNKNOWN", "Catégorie Odoo", "Sous-catégorie Odoo"),
            ["Catégorie Odoo", "Sous-catégorie Odoo", None],
        )

    def test_default_when_no_match(self):
        self.assertEqual(classify(""), ["Non classé"])
