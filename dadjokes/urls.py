"""
urls.py
Xinxu Chen (chenxin@bu.edu)

Defines the URL patterns for the dadjokes app.
"""

from django.urls import path
from . import views

app_name = 'dadjokes'

urlpatterns = [
    path('', views.show_random, name='show_random'),
    path('random', views.show_random, name='random'),
    path('jokes', views.show_all_jokes, name='show_all_jokes'),
    path('joke/<int:pk>', views.show_joke, name='show_joke'),
    path('pictures', views.show_all_pictures, name='show_all_pictures'),
    path('picture/<int:pk>', views.show_picture, name='show_picture'),

    path('api/', views.api_show_random, name='api_show_random'),
    path('api/random', views.api_show_random, name='api_random'),
    path('api/jokes', views.api_show_all_jokes, name='api_show_all_jokes'),
    path('api/joke/<int:pk>', views.api_show_joke, name='api_show_joke'),
    path('api/pictures', views.api_show_all_pictures, name='api_show_all_pictures'),
    path('api/picture/<int:pk>', views.api_show_picture, name='api_show_picture'),
    path('api/random_picture', views.api_show_random_picture, name='api_random_picture'),
]