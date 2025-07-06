from django.test import TestCase
from django.core.management import call_command
from products.models import Product

class ClassifyProductsCommandTests(TestCase):
    def test_command_updates_categories(self):
        p = Product.objects.create(name='Cam', default_code='DS-2CD1', list_price=1, categ_id='')
        call_command('classify_products')
        p.refresh_from_db()
        self.assertEqual(p.categ_id, 'Vidéo IP / Caméras fixes')
