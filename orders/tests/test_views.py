from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from products.models import Product

User = get_user_model()

class OrderViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1', role=User.INSTALLER)
        self.user2 = User.objects.create_user(username='user2', password='pass2', role=User.INSTALLER)
        self.product = Product.objects.create(name='Prod', list_price=10, categ_id='cat')
        self.create_url = reverse('create_order')
        self.list_url = lambda uid: reverse('list_orders', args=[uid])

    def _add_to_cart(self, user, quantity=1):
        cart, _ = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=quantity)

    def test_create_requires_login(self):
        response = self.client.post(self.create_url, data={'user_id': self.user1.id}, content_type='application/json')
        self.assertEqual(response.status_code, 302)

    def test_create_and_list_order(self):
        self._add_to_cart(self.user1, 2)
        self.client.login(username='user1', password='pass1')
        response = self.client.post(self.create_url, data={'user_id': self.user1.id}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.filter(cart__user=self.user1).count(), 0)
        response = self.client.get(self.list_url(self.user1.id))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['items'][0]['quantity'], 2)

    def test_user_cannot_access_other_orders(self):
        self._add_to_cart(self.user1, 1)
        self.client.login(username='user1', password='pass1')
        self.client.post(self.create_url, data={'user_id': self.user1.id}, content_type='application/json')
        self.client.logout()
        self.client.login(username='user2', password='pass2')
        response = self.client.get(self.list_url(self.user1.id))
        self.assertEqual(response.status_code, 403)
