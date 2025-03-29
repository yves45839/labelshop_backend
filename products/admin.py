from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
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
    list_display = (
        'name', 'barcode', 'list_price', 'discount_price', 'stock_quantity',
        'is_available', 'is_online', 'hide_price',
        'image_1920_preview', 'image_1024_preview', 'image_512_preview', 'image_256_preview', 'created_at'
    )
    list_filter = ('is_available', 'is_online', 'hide_price', 'categ_id', 'brand', 'created_at', HasImagesFilter)
    search_fields = ('name', 'barcode', 'default_code', 'keywords', 'search_tags', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_1920_preview', 'image_1024_preview', 'image_512_preview', 'image_256_preview')
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
            'fields': ('image_url', 'image_1920', 'image_1024', 'image_512', 'image_256', 'video_url', 'pdf_brochure', 'image_1920_preview', 'image_1024_preview', 'image_512_preview', 'image_256_preview')
        }),
        ('Dates importantes', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(image_count=Count('images'))

    def image_preview(self, image_url, size_label):
        if image_url:
            source_label = "Odoo" if "http" in image_url else "Local"
            return format_html('<img src="{}" width="50" height="50" style="border-radius:4px;"/> ({})', image_url, source_label)
        return "Pas d'image"

    def image_1920_preview(self, obj):
        return self.image_preview(obj.image_1920, "1920")
    image_1920_preview.short_description = "Image 1920"

    def image_1024_preview(self, obj):
        return self.image_preview(obj.image_1024, "1024")
    image_1024_preview.short_description = "Image 1024"

    def image_512_preview(self, obj):
        return self.image_preview(obj.image_512, "512")
    image_512_preview.short_description = "Image 512"

    def image_256_preview(self, obj):
        return self.image_preview(obj.image_256, "256")
    image_256_preview.short_description = "Image 256"
