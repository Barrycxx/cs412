"""
serializers.py
Xinxu Chen (chenxin@bu.edu)

Serializers for the mini_insta REST API.
"""

from rest_framework import serializers
from .models import Profile, Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "image", "timestamp"]

    def get_image(self, obj):
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    profile_id = serializers.IntegerField(source="profile.pk", read_only=True)
    username = serializers.CharField(source="profile.username", read_only=True)
    display_name = serializers.CharField(source="profile.display_name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "profile_id",
            "username",
            "display_name",
            "caption",
            "timestamp",
            "photos",
        ]

    def get_photos(self, obj):
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True).data


class ProfileSerializer(serializers.ModelSerializer):
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "display_name",
            "profile_image_url",
            "bio_text",
            "join_date",
            "num_followers",
            "num_following",
        ]

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["caption"]