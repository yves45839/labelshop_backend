from django.test import TestCase
from products.models import Product

class ProductAutoClassificationTests(TestCase):
    def test_save_auto_sets_category(self):
        product = Product.objects.create(
            name='Camera', default_code='DS-2CD123', list_price=1, categ_id=''
        )
        product.refresh_from_db()
        self.assertEqual(product.categ_id, 'Vid\xe9o IP / Cam\xe9ras fixes')

