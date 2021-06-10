from django.db import models

# Create your models here.


class CategoryParent(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default='TRUE')
    created_date = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'category_parent'

    def __str__(self):
        return self.title


class CategoryChild(models.Model):

    # many to one relation with category parent
    category_parent = models.ForeignKey(
        CategoryParent, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, )
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/category')
    status = models.CharField(max_length=10, default='TRUE')
    created_date = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'category_child'

    def __str__(self):
        return self.title
