from django.contrib import admin
from django.db.models import Count
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class HasImagesFilter(admin.SimpleListFilter):
    title = 'Avec Images'
    parameter_name = 'has_images'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Oui'),
            ('no', 'Non'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(image_count=Count('images'))
        if self.value() == 'yes':
            return queryset.filter(image_count__gt=0)
        if self.value() == 'no':
            return queryset.filter(image_count=0)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'list_price', 'discount_price', 'stock_quantity', 'is_available', 'is_online', 'hide_price', 'created_at')
    list_filter = ('is_available', 'is_online', 'hide_price', 'categ_id', 'brand', 'created_at', HasImagesFilter)
    search_fields = ('name', 'barcode', 'default_code', 'keywords', 'search_tags', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_available', 'is_online', 'hide_price')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'slug', 'barcode', 'default_code', 'odoo_id', 'categ_id', 'brand')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description')
        }),
        ('Tarification et Stock', {
            'fields': ('list_price', 'discount_price', 'stock_quantity', 'hide_price')
        }),
        ('Disponibilité', {
            'fields': ('is_available', 'is_online')
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'keywords', 'search_tags')
        }),
        ('Médias & Fichiers', {
            'fields': ('image_url', 'image_1920', 'image_1024', 'image_512', 'image_256', 'video_url', 'pdf_brochure')
        }),
        ('Dates importantes', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(image_count=Count('images'))
