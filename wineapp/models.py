from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Post(models.Model):
    cocktailName = models.CharField(max_length=100)
    cocktailPic = models.CharField(max_length=200)
    cocktailAPI = models.CharField(max_length=300)
    cocktailCategory = models.CharField(max_length=100)
    cocktailInst = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
