"""
urls.py
Xinxu Chen (chenxin@bu.edu)

Main URL configuration for the cs412 project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cs412/voter_analytics/', include('voter_analytics.urls')),
    path('', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('mini_insta/', include('mini_insta.urls')),
   path('dadjokes/', include(('dadjokes.urls', 'dadjokes'), namespace='dadjokes')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)