
from django.db import models
from users.models import User
from product.models import Product
from django.db.models import Avg, Count
# Create your models here.


class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DetailBill(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bill_code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'detail_bill'


class Item(models.Model):
    detail_bill = models.OneToOneField(
        DetailBill,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    title = models.CharField(max_length=255)
    price_sale = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    amount_sale = models.IntegerField(default=0)
    keywords = models.CharField(max_length=255)
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    image_sale = models.ImageField(blank=True, upload_to='images/product')
    description = models.TextField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    def countreview(self):
        reviews = Comment.objects.filter(
            product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def avaregereview(self):
        reviews = Comment.objects.filter(
            product=self, status='True').aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    class Meta:
        db_table = 'item'


class Images(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/product')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'item_image'


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default='True')
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
