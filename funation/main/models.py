from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_target_money = models.PositiveIntegerField()
    product_crowd_money = models.PositiveIntegerField()
    product_description = models.TextField()
    product_img = models.ImageField(null=True)

# Create your models here.
