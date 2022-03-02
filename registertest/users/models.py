from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.CharField(blank=True, max_length=255)
    name = models.CharField(blank=True, max_length=255)
    profile_photo = models.ImageField(blank=True, default='profile.png')
    followers = models.ManyToManyField("self")
    following = models.ManyToManyField("self")


class PreferLocation(models.Model):
    user = models.ForeignKey(
            User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'user_location'
        )
    location = models.TextField(blank=True)