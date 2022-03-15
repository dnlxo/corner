from rest_framework import serializers

from users.models import User
from users.serializers import PreferLocationSerializer
from .models import Post, Comment, PostImage, ReComment

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "profile_photo",
        )


class PostValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "description",
            "latitude",
			"longitude",
			"road_address",
			"alias"
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


class ReCommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()

    class Meta:
        model = ReComment
        fields = (
            "id",
            "contents",
            "author",
            "create_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()
    recomment = ReCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "contents",
            "author",
            "create_at",
            "recomment",
        )


class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    image_post = PostImageSerializer(many=True, read_only=True)
    author = FeedAuthorSerializer()
    likes = FeedAuthorSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "image_post",
            "description",
            "comment_post",
            "like_count",
            "likes",
            "author",
            "latitude",
			"longitude",
			"road_address",
            "district",
			"alias",
            "create_at",
            "updated_at",
        )


class MyPageAccountSerializer(serializers.ModelSerializer):
    followers = FeedAuthorSerializer(many=True)
    following = FeedAuthorSerializer(many=True)
    post_author = PostSerializer(many=True)
    user_location = PreferLocationSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "user_location",
            "profile_photo",
            "followers_count",
            "followers",
            "following_count",
            "following",
            "post_author",
        )

