from rest_framework import serializers
from .models import User, PreferLocation


class PreferLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferLocation
        fields = (
            "location",
        )


class UserSerializer(serializers.ModelSerializer):
    user_location = PreferLocationSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'user_location',
            )
