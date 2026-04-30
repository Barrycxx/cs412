"""
project/models.py
Xinxu Chen (chenxin@bu.edu)

Data models for the final project app. These models store users, genres,
games, reviews, and collection records for the video game collection and
review tracker.
"""

from django.db import models


class UserProfile(models.Model):
    """
    Stores basic information about a user of the application.

    Attributes:
        username: The user's display name.
        email: The user's email address.
        bio: A short biography or description about the user.
    """

    username = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    def __str__(self):
        """
        Return a readable string for this user profile.
        """
        return self.username


class Genre(models.Model):
    """
    Stores a video game genre.

    Attributes:
        name: The name of the genre.
        description: A short description of the genre.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        Return a readable string for this genre.
        """
        return self.name


class Game(models.Model):
    """
    Stores information about a video game.

    Attributes:
        title: The title of the game.
        developer: The company or studio that made the game.
        release_date: The date the game was released.
        platform: The platform the game is on.
        cover_image: The uploaded cover image for the game.
        genre: The genre this game belongs to.
    """

    title = models.CharField(max_length=200)
    developer = models.CharField(max_length=200)
    release_date = models.DateField()
    platform = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='game_covers/', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return a readable string for this game.
        """
        return self.title


class Review(models.Model):
    """
    Stores a user's review for a game.

    Attributes:
        user_profile: The user who wrote the review.
        game: The game being reviewed.
        rating: A numeric rating for the game.
        comment: The written review text.
        created_at: The date and time when the review was created.
    """

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string for this review.
        """
        return f"{self.user_profile} - {self.game}"


class Collection(models.Model):
    """
    Stores a game saved in a user's collection.

    Attributes:
        user_profile: The user who saved the game.
        game: The saved game.
        status: The user's current status for the game.
    """

    STATUS_CHOICES = [
        ('wishlist', 'Wishlist'),
        ('playing', 'Playing'),
        ('completed', 'Completed'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        """
        Return a readable string for this collection record.
        """
        return f"{self.user_profile} - {self.game} ({self.status})"