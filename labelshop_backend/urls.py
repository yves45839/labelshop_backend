from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
]

# Pour servir les médias uniquement en développement :
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
