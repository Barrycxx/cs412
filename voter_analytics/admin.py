"""
admin.py
Xinxu Chen (chenxin@bu.edu)

Registers models for the admin interface.
"""

from django.contrib import admin
from .models import Voter


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'party_affiliation',
        'date_of_birth',
        'voter_score',
    )
    search_fields = ('first_name', 'last_name', 'street_name')
    list_filter = (
        'party_affiliation',
        'voter_score',
        'v20state',
        'v21town',
        'v21primary',
        'v22general',
        'v23town',
    )