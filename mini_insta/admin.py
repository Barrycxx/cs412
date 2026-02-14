"""
admin.py
Xinxu Chen (chenxin@bu.edu)

Registers models for the admin interface.
"""

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = ("username", "display_name", "join_date")
