from django.db import models

# Create your models here.
class TestUpload(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/category')