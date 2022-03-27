from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.CharField(blank=True, max_length=255)
    name = models.CharField(blank=True, max_length=255)
    profile_photo = models.ImageField(blank=True, default='profile.png')
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='user_followers')
    followers_count = models.IntegerField(default=0, blank=True)
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='user_following')
    following_count = models.IntegerField(default=0, blank=True)
    like_post = models.ManyToManyField("posts.models.Post", blank=True, related_name='like_users')

class PreferLocation(models.Model):
    user = models.ForeignKey(
            User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'user_location'
        )
    location = models.TextField(blank=True)