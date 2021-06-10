
from category.models import CategoryChild
from django.db import models

# Create your models here.


class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    category = models.ForeignKey(CategoryChild, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    name_supplier = models.CharField(max_length=255)
    phone_supplier = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'product_product'
