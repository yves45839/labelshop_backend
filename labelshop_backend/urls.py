from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('inventory/', include('inventory.urls')),
    path('blogs/', include('blog.urls')),
]

# Pour servir les médias uniquement en développement :
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
