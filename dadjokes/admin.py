"""
admin.py
Xinxu Chen (chenxin@bu.edu)

Registers the models for the dadjokes app.
"""

from django.contrib import admin
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)