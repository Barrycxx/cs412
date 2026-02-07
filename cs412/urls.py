from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("Hello CS412! My deployment works!")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]
