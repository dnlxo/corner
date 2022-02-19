from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.CharField(blank=True, max_length=255)
    name = models.CharField(blank=True, max_length=255)
    profile_photo = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField("self")
    following = models.ManyToManyField("self")