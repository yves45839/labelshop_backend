from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from products.models import Product
import json


class CartViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='pass', role=User.INSTALLER
        )
        self.product = Product.objects.create(
            name='Prod', list_price=10.0, categ_id='cat'
        )
        self.add_url = reverse('add_to_cart')
        self.update_url = reverse('update_cart_item')

    def _post(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

    def test_add_to_cart_rejects_invalid_quantity(self):
        for qty in [0, -1, 'abc']:
            resp = self._post(self.add_url, {
                'user_id': self.user.id,
                'product_id': self.product.id,
                'quantity': qty,
            })
            self.assertEqual(resp.status_code, 400)

    def test_update_cart_item_rejects_invalid_quantity(self):
        # add valid item first
        self._post(self.add_url, {
            'user_id': self.user.id,
            'product_id': self.product.id,
            'quantity': 1,
        })
        for qty in [0, -2, 'abc']:
            resp = self._post(self.update_url, {
                'user_id': self.user.id,
                'product_id': self.product.id,
                'quantity': qty,
            })
            self.assertEqual(resp.status_code, 400)
