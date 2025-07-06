from django.test import SimpleTestCase
from products.classifier import classify


class ClassifyTests(SimpleTestCase):
    def test_video_analogique(self):
        self.assertEqual(classify("DS-2AE123"), ["Vidéo analogique", "Caméras PTZ"])
        self.assertEqual(classify("DS-2CE999"), ["Vidéo analogique", "Caméras fixes"])
        self.assertEqual(classify("DS-7200"), ["Vidéo analogique", "DVR"])

    def test_video_ip(self):
        self.assertEqual(classify("ds-2df001"), ["Vidéo IP", "Caméras PTZ"])
        self.assertEqual(classify("DS-2CD321"), ["Vidéo IP", "Caméras fixes"])
        self.assertEqual(classify("DS-7632"), ["Vidéo IP", "NVR"])
        self.assertEqual(classify("DS-3E0101"), ["Vidéo IP", "Switches PoE"])
        self.assertEqual(classify("DS-A123"), ["Vidéo IP", "Stockage IP SAN/NAS"])

    def test_default(self):
        self.assertEqual(classify("UNKNOWN"), ["Non classé"])
        self.assertEqual(classify(""), ["Non classé"])
