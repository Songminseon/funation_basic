from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_target_money = models.PositiveIntegerField()
    product_crowd_money = models.PositiveIntegerField()
    product_description = models.TextField()
    product_img = models.ImageField(null=True, upload_to = "img_folder/")

    def __str__(self):
        return self.product_name + str(self.product_target_money)

    def summary(self):
        return self.product_description[:30]

# Create your models here.
