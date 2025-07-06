from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image_1024_alter_product_image_1920_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_main',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='category_sub',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='category_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
