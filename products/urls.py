from django.urls import path
from .views import fetch_odoo_products, search_products, get_products

urlpatterns = [
    path('fetch-odoo-products/', fetch_odoo_products, name='fetch_odoo_products'),
    path('search-products/', search_products, name='search_products'),
    path('get-products/', get_products, name='get_products'),
]
