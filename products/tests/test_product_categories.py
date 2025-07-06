from django.test import TestCase
from products.models import Product


class ProductCategoryTests(TestCase):
    def test_categories_assigned_on_save(self):
        product = Product(
            name="Camera Test",
            list_price=10.0,
            categ_id="Test",
            barcode="DS-2CD999"
        )
        product.save()
        self.assertEqual(product.category_main, "Vidéo IP")
        self.assertEqual(product.category_sub, "Caméras fixes")
