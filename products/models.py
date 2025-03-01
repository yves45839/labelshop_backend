from django.db import models

class Product(models.Model):
    odoo_id = models.IntegerField(unique=True, null=True)  # ID Odoo
    name = models.CharField(max_length=255)  # Nom du produit
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)  # Slug SEO
    description = models.TextField(blank=True, null=True)  # Description du produit
    short_description = models.CharField(max_length=255, blank=True, null=True)  # Description courte
    list_price = models.FloatField()  # Prix du produit
    discount_price = models.FloatField(blank=True, null=True)  # Prix promo si disponible
    stock_quantity = models.IntegerField(default=0)  # Stock
    is_available = models.BooleanField(default=True)  # Disponibilité
    default_code = models.CharField(max_length=100, blank=True, null=True)  # Référence produit
    barcode = models.CharField(max_length=100, blank=True, null=True)  # Code-barre
    categ_id = models.CharField(max_length=255)  # Catégorie
    brand = models.CharField(max_length=100, blank=True, null=True)  # Marque
    rating = models.FloatField(default=0.0)  # Note moyenne des avis
    reviews_count = models.IntegerField(default=0)  # Nombre d’avis

    # 📷 Images
    image_url = models.URLField(blank=True, null=True)  # URL principale
    image_1920 = models.URLField(blank=True, null=True)  # Haute résolution
    image_1024 = models.URLField(blank=True, null=True)  # Web optimisée
    image_512 = models.URLField(blank=True, null=True)  # Miniature 512px
    image_256 = models.URLField(blank=True, null=True)  # Miniature 256px

    # 🔍 SEO et recherche
    meta_title = models.CharField(max_length=255, blank=True, null=True)  # Balise <title>
    meta_description = models.TextField(blank=True, null=True)  # Meta description SEO
    keywords = models.TextField(blank=True, null=True)  # Mots-clés
    search_tags = models.TextField(blank=True, null=True)  # Tags pour recherche

    # 📅 Dates
    created_at = models.DateTimeField(auto_now_add=True)  # Création
    updated_at = models.DateTimeField(auto_now=True)  # Mise à jour

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Recherche rapide par nom
            models.Index(fields=['slug']),  # URLs optimisées SEO
            models.Index(fields=['categ_id']),  # Recherche par catégorie
            models.Index(fields=['default_code']),  # Recherche par référence
            models.Index(fields=['barcode']),  # Recherche par code-barre
        ]
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.name
