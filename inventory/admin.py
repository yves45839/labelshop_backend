from django.contrib import admin

from .models import Site, ProductStock


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ("product", "site", "quantity")
    list_filter = ("site",)
