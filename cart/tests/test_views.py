from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cart.models import CartItem
from products.models import Product
import json

User = get_user_model()

class CartViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1', role=User.INSTALLER)
        self.user2 = User.objects.create_user(username='user2', password='pass2', role=User.INSTALLER)
        self.product = Product.objects.create(name='Prod', list_price=10, categ_id='cat')
        self.add_url = reverse('add_to_cart')
        self.update_url = reverse('update_cart_item')
        self.remove_url = reverse('remove_from_cart')
        self.view_url = reverse('view_cart')

    def test_add_requires_login(self):
        response = self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 302)

    def test_add_invalid_quantity(self):
        self.client.login(username='user1', password='pass1')
        for qty in [0, -1, 'abc']:
            with self.subTest(qty=qty):
                response = self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': qty}), content_type='application/json')
                self.assertEqual(response.status_code, 400)

    def test_add_and_view_cart(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 2}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['quantity'], 2)

    def test_update_cart_item(self):
        self.client.login(username='user1', password='pass1')
        self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 1}), content_type='application/json')
        response = self.client.post(self.update_url, data=json.dumps({'product_id': self.product.id, 'quantity': 5}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        item = CartItem.objects.get(cart=self.user1.cart, product=self.product)
        self.assertEqual(item.quantity, 5)

    def test_update_invalid_quantity(self):
        self.client.login(username='user1', password='pass1')
        self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 1}), content_type='application/json')
        response = self.client.post(self.update_url, data=json.dumps({'product_id': self.product.id, 'quantity': 0}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_remove_from_cart(self):
        self.client.login(username='user1', password='pass1')
        self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 1}), content_type='application/json')
        response = self.client.post(self.remove_url, data=json.dumps({'product_id': self.product.id}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(cart=self.user1.cart, product=self.product).exists())

    def test_user_cannot_modify_other_cart(self):
        self.client.login(username='user1', password='pass1')
        self.client.post(self.add_url, data=json.dumps({'product_id': self.product.id, 'quantity': 2}), content_type='application/json')
        self.client.logout()
        self.client.login(username='user2', password='pass2')
        response = self.client.post(self.update_url, data=json.dumps({'product_id': self.product.id, 'quantity': 3}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        item = CartItem.objects.get(cart=self.user1.cart, product=self.product)
        self.assertEqual(item.quantity, 2)

