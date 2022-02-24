from rest_framework import serializers

from users.models import User
from .models import Post, Comment, PostImage

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "profile_photo",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()

    class Meta:
        model = Comment
        fields = (
            "id",
            "contents",
            "author",
        )


class PostValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "description",
        )

class CommentValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "contents",
        )

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = PostImage
        fields = (
            "image",
        )


class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    image_post = PostImageSerializer(many=True, read_only=True)
    author = FeedAuthorSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "image_post",
            "description",
            "comment_post",
            "author",
        )