from distutils.command.upload import upload
from django.db import models
from users import models as user_model

# Create your models here.
class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

'''
게시글 모델에는 (author(외래키 User), 
            image,
            description(글),
            image_likes(좋아요))
가 기본적으로 있다.
'''
class Post(TimeStamedModel):
    author = models.ForeignKey(
                user_model.User, 
                null=True, 
                on_delete=models.CASCADE, 
                related_name= 'post_author'
            )
    # image = models.ImageField(blank=False)
    description = models.TextField(blank=False)
    image_likes = models.ManyToManyField(
                    user_model.User,
                    blank=True,
                    related_name='post_image_likes'
            )

    def __str__(self):
        return f"{self.author}: {self.description}"

'''
게시글 댓글 모델에는 (
                author(User 외래키),
                posts(Post 외래키),
                contents(댓글 내용)
                )
기본적으로 이렇게 3가지가 있다.
'''
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
    contents = models.TextField(blank=True)

    def __str__(self):
        return f"{self.author}: {self.contents}"

class PostImage(models.Model):
    posts = models.ForeignKey(
            Post, 
            null=True, 
            on_delete=models.CASCADE, 
            related_name= 'image_post'
        )
    image = models.ImageField(blank=False)