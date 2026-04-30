"""
project/urls.py
Xinxu Chen (chenxin@bu.edu)

URL patterns for the final project app.
"""

from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.GameListView.as_view(), name='home'),

    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),

    path('games/', views.GameListView.as_view(), name='game_list'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),

    path('profiles/', views.UserProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile_detail'),

    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),

    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collection/create/', views.CollectionCreateView.as_view(), name='collection_create'),
]