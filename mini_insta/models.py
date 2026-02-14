"""
models.py
Xinxu Chen (chenxin@bu.edu)

Defines the data models for the mini_insta app.
"""

from django.db import models


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
