from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='restaurant_home'),
    path("main/", views.main, name="main"),
    path("order/", views.order, name="order"),
    path("confirmation/", views.confirmation, name="confirmation"),
]
