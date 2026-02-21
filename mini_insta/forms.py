"""
mini_insta/forms.py
Xinxu Chen (chenxin@bu.edu)

Forms for mini_insta.
"""

from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]