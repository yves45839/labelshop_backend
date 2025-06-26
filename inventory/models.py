from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product = models.ForeignKey('products.Product', related_name='stocks', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, related_name='stocks', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'site')
        verbose_name = "Stock produit"
        verbose_name_plural = "Stocks produits"

    def __str__(self):
        return f"{self.product.name} - {self.site.name}: {self.quantity}"
