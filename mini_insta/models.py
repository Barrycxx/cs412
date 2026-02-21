"""
models.py
Xinxu Chen (chenxin@bu.edu)

Defines the data models for the mini_insta app.
This file contains the Profile model from Assignment 3 and adds Post/Photo
models for Assignment 4 (Part 2).
"""

from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """
    Represents a user profile for the mini_insta app.

    Fields:
        username: short unique handle for the user.
        display_name: the name to show on pages.
        profile_image_url: URL to the user's profile image.
        bio_text: short bio text shown on the profile.
        join_date: date the user joined.
    """

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    bio_text = models.TextField(blank=True)
    join_date = models.DateField()

    def __str__(self) -> str:
        """
        Returns a readable string representation of the Profile.
        """
        return f"{self.username} ({self.display_name})"

    def get_all_posts(self):
        """
        Returns all Post objects for this Profile, ordered by timestamp (newest first).

        Returns:
            QuerySet[Post]: all posts for this profile.
        """
        return Post.objects.filter(profile=self).order_by("-timestamp")


class Post(models.Model):
    """
    Represents an Instagram-style post created by a Profile.

    Fields:
        profile: foreign key to the Profile who created the post.
        timestamp: time the post was created/saved.
        caption: optional text associated with the post.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    caption = models.TextField(blank=True)

    def __str__(self) -> str:
        """
        Returns a readable string representation of the Post.
        """
        return f"Post {self.pk} by @{self.profile.username}"

    def get_all_photos(self):
        """
        Returns all Photo objects for this Post, ordered by timestamp (newest first).

        Returns:
            QuerySet[Photo]: all photos for this post.
        """
        return Photo.objects.filter(post=self).order_by("-timestamp")


class Photo(models.Model):
    """
    Represents an image associated with a Post.

    Fields:
        post: foreign key to the Post this photo belongs to.
        image_url: URL to an image hosted on the public web.
        timestamp: time the photo was created/saved.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """
        Returns a readable string representation of the Photo.
        """
        return f"Photo {self.pk} for Post {self.post.pk}"