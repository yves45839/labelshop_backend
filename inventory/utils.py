from django.db import transaction
from django.core.exceptions import ValidationError

from .models import ProductStock


def transfer_stock(product, from_site, to_site, quantity: int):
    """Transfer quantity of product from one site to another."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if from_site == to_site:
        raise ValueError("Source and destination sites must be different")

    with transaction.atomic():
        origin, _ = ProductStock.objects.select_for_update().get_or_create(
            product=product, site=from_site, defaults={"quantity": 0}
        )
        if origin.quantity < quantity:
            raise ValidationError("Insufficient stock at origin site")
        origin.quantity -= quantity
        origin.save(update_fields=["quantity"])

        dest, _ = ProductStock.objects.select_for_update().get_or_create(
            product=product, site=to_site, defaults={"quantity": 0}
        )
        dest.quantity += quantity
        dest.save(update_fields=["quantity"])

    return origin, dest
