"""
admin.py
Xinxu Chen (chenxin@bu.edu)

Registers models for the admin interface.
"""

from django.contrib import admin
from .models import Profile, Post, Photo, Follow, Comment, Like


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = ("username", "display_name", "user", "join_date")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = ("id", "profile", "timestamp")
    list_filter = ("profile",)
    search_fields = ("caption", "profile__username")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Admin configuration for Photo model.
    """
    list_display = ("id", "post", "timestamp")
    list_filter = ("post",)
    search_fields = ("image_url",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower_profile", "profile", "timestamp")
    list_filter = ("profile", "follower_profile")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "profile", "timestamp")
    list_filter = ("post", "profile")
    search_fields = ("text",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "profile", "timestamp")
    list_filter = ("post", "profile")