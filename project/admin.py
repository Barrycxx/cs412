"""
project/admin.py
Xinxu Chen (chenxin@bu.edu)

Admin registrations for the final project app.
"""

from django.contrib import admin
from .models import UserProfile, Genre, Game, Review, Collection


admin.site.register(UserProfile)
admin.site.register(Genre)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Collection)