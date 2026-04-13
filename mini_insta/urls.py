"""
mini_insta/urls.py
Xinxu Chen (chenxin@bu.edu)

URL routes for the mini_insta app.
"""

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "mini_insta"

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),

    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/followers", views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", views.ShowFollowingDetailView.as_view(), name="show_following"),

    path(
        "login/",
        auth_views.LoginView.as_view(template_name="mini_insta/login.html"),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=reverse_lazy("mini_insta:logout_confirmation")),
        name="logout"
    ),
    path("logged_out/", views.LogoutConfirmationView.as_view(), name="logout_confirmation"),

    path("create_profile", views.CreateProfileView.as_view(), name="create_profile"),

    path("profile/", views.MyProfileDetailView.as_view(), name="profile"),
    path("profile/update", views.UpdateProfileView.as_view(), name="update_profile"),
    path("profile/create_post", views.CreatePostView.as_view(), name="create_post"),
    path("profile/feed", views.PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", views.SearchView.as_view(), name="search"),

    path("post/<int:pk>/delete", views.DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", views.UpdatePostView.as_view(), name="update_post"),

    path("profile/<int:pk>/follow", views.FollowProfileView.as_view(), name="follow_profile"),
    path("profile/<int:pk>/delete_follow", views.DeleteFollowProfileView.as_view(), name="delete_follow"),

    path("post/<int:pk>/like", views.LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", views.DeleteLikePostView.as_view(), name="delete_like"),

    path("api/login/", views.APILoginView.as_view(), name="api_login"),
    path("api/profiles/", views.APIProfileListView.as_view(), name="api_profiles"),
    path("api/profile/<int:pk>/", views.APIProfileDetailView.as_view(), name="api_profile"),
    path("api/profile/<int:pk>/posts/", views.APIProfilePostsView.as_view(), name="api_profile_posts"),
    path("api/profile/<int:pk>/feed/", views.APIProfileFeedView.as_view(), name="api_profile_feed"),
    path("api/profile/<int:pk>/create_post/", views.APICreatePostView.as_view(), name="api_create_post"),
]