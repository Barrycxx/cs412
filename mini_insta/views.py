"""
mini_insta/views.py
Xinxu Chen (chenxin@bu.edu)

Views for mini_insta. This app shows a list of profiles and a detail page
for one profile using Django generic class-based views.
"""

from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    """
    Display a page showing all Profile records.

    Uses Django's generic ListView and renders a template called
    mini_insta/show_all_profiles.html.
    """

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """
    Display a page for a single Profile record.

    Uses Django's generic DetailView and renders a template called
    mini_insta/show_profile.html.

    The Profile is selected by primary key (pk) from the URL.
    """

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
