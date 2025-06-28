from django.test import TestCase
from django.core.exceptions import ValidationError

from products.models import Product
from inventory.models import Site, ProductStock
from inventory.utils import transfer_stock


class TransferStockTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Prod', list_price=10, categ_id='cat')
        self.site1, _ = Site.objects.get_or_create(name='Abobo')
        self.site2, _ = Site.objects.get_or_create(name='Treichville')
        ProductStock.objects.create(product=self.product, site=self.site1, quantity=10)
        ProductStock.objects.create(product=self.product, site=self.site2, quantity=5)

    def test_transfer_stock_success(self):
        transfer_stock(self.product, self.site1, self.site2, 7)
        origin = ProductStock.objects.get(product=self.product, site=self.site1)
        dest = ProductStock.objects.get(product=self.product, site=self.site2)
        self.assertEqual(origin.quantity, 3)
        self.assertEqual(dest.quantity, 12)

    def test_transfer_insufficient_stock(self):
        with self.assertRaises(ValidationError):
            transfer_stock(self.product, self.site1, self.site2, 20)
