from django.urls import path
from .views import manage_sites, list_product_stock, update_product_stock, transfer_product_stock

urlpatterns = [
    path('sites/', manage_sites, name='manage_sites'),
    path('products/<int:product_id>/stock/', list_product_stock, name='list_product_stock'),
    path('update-stock/', update_product_stock, name='update_product_stock'),
    path('transfer-stock/', transfer_product_stock, name='transfer_product_stock'),
]
