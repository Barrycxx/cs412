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

    def get_absolute_url(self):
        """
        After updating a profile, go back to this profile page.
        """
        return f"/mini_insta/profile/{self.pk}/"

    # -------- Task 4: Follow accessors --------
    def get_followers(self):
        """
        Returns a list of Profile objects who follow this profile.
        """
        follows = Follow.objects.filter(profile=self).order_by("-timestamp")
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        """
        Returns the number of followers.
        """
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """
        Returns a list of Profile objects that this profile is following.
        """
        follows = Follow.objects.filter(follower_profile=self).order_by("-timestamp")
        return [f.profile for f in follows]

    def get_num_following(self):
        """
        Returns the number of profiles this profile follows.
        """
        return Follow.objects.filter(follower_profile=self).count()

    # -------- Task 5: Feed accessor --------
    def get_post_feed(self):
        """
        Returns Posts for profiles this user is following, newest first.
        """
        following_profiles = self.get_following()
        return Post.objects.filter(profile__in=following_profiles).order_by("-timestamp")


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

    # -------- Task 4: Comments + Likes accessors --------
    def get_all_comments(self):
        """
        Returns all comments for this post (oldest first).
        """
        return Comment.objects.filter(post=self).order_by("timestamp")

    def get_likes(self):
        """
        Returns all likes for this post.
        """
        return Like.objects.filter(post=self)

    def get_num_likes(self):
        """
        Returns number of likes.
        """
        return Like.objects.filter(post=self).count()


class Photo(models.Model):
    """
    Represents an image associated with a Post.

    Fields:
        post: foreign key to the Post this photo belongs to.
        image_url: URL to an image hosted on the public web. (kept for older data)
        image_file: uploaded image stored in media/ directory.
        timestamp: time the photo was created/saved.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # keep for backwards-compatibility
    image_url = models.URLField(blank=True)

    # Task 1: local upload support
    image_file = models.ImageField(upload_to="mini_insta/", blank=True, null=True)

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        """
        Returns a readable string representation of the Photo.
        """
        if self.image_url:
            return f"Photo {self.pk} (url) for Post {self.post.pk}"
        return f"Photo {self.pk} (file) for Post {self.post.pk}"

    def get_image_url(self) -> str:
        """
        Returns whichever image source exists.
        """
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""


# ---------------- Task 4: Follow / Comment / Like models ----------------

class Follow(models.Model):
    """
    Represents a follow relationship:
    follower_profile follows profile.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"


class Comment(models.Model):
    """
    Represents a comment by a Profile on a Post.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self) -> str:
        return f"Comment {self.pk} by @{self.profile.username} on Post {self.post.pk}"


class Like(models.Model):
    """
    Represents a like by a Profile on a Post.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"@{self.profile.username} likes Post {self.post.pk}"