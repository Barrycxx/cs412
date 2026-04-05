"""
models.py
Xinxu Chen (chenxin@bu.edu)

Defines the data models for the dadjokes app.
Contains the Joke model and the Picture model.
"""

from django.db import models


class Joke(models.Model):
    joke_text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor}: {self.joke_text[:50]}"


class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor}: {self.image_url}"