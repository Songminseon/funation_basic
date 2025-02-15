from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mem_name = models.CharField(max_length=50)
    mem_email = models.EmailField()
    mem_info = models.CharField(max_length=7)
    mem_phone = models.CharField(max_length=15, null=True)

  
    def __str__(self):
        return self.mem_name

    