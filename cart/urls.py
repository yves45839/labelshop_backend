from django.urls import path
from .views import add_to_cart, update_cart_item, remove_from_cart, view_cart

urlpatterns = [
    path('add/', add_to_cart, name='add_to_cart'),
    path('update/', update_cart_item, name='update_cart_item'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
    path('<int:user_id>/', view_cart, name='view_cart'),
]
