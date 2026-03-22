"""
urls.py
Xinxu Chen (chenxin@bu.edu)

Defines URL patterns for the voter analytics app.
"""

from django.urls import path
from .views import VoterListView, VoterDetailView, GraphView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphView.as_view(), name='graphs'),
]