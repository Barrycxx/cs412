"""
mini_insta/urls.py
Xinxu Chen (chenxin@bu.edu)

URL routes for the mini_insta app.
"""

from django.urls import path
from . import views

app_name = "mini_insta"

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post/", views.CreatePostView.as_view(), name="create_post"),
]