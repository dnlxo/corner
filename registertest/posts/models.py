from distutils.command.upload import upload
from django.db import models
from users import models as user_model

# Create your models here.
class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(TimeStamedModel):
    author = models.ForeignKey(
                user_model.User, 
                null=True, 
                on_delete=models.CASCADE, 
                related_name= 'post_author'
            )
    description = models.TextField(blank=False)
    latitude = models.TextField(blank=True)
    longitude = models.TextField(blank=True)
    road_address = models.TextField(blank=True)
    district = models.TextField(blank=True)
    alias = models.TextField(blank=True)
    likes = models.ManyToManyField(
                    user_model.User,
                    blank=True,
                    related_name='post_likes'
            )
    like_count = models.IntegerField(default=0)


class Comment(TimeStamedModel):
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'comment_author'
        )
    posts = models.ForeignKey(
            Post, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'comment_post'
        )
    contents = models.TextField(blank=False)


class PostImage(models.Model):
    posts = models.ForeignKey(
            Post, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'image_post'
        )
    image = models.ImageField(blank=False)


class ReComment(TimeStamedModel):
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'recomment_author'
        )
    comment = models.ForeignKey(
            Comment, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'recomment'
        )
    contents = models.TextField(blank=False)