from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
