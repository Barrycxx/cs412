"""
project/forms.py
Xinxu Chen (chenxin@bu.edu)

Forms for the final project app.
"""

from django import forms
from .models import Review, Collection


class ReviewForm(forms.ModelForm):
    """
    Form for creating and updating a review.

    This form allows the user to select a user profile, select a game,
    enter a numeric rating, and write a comment.
    """

    class Meta:
        """
        Metadata for the ReviewForm model form.
        """
        model = Review
        fields = ['user_profile', 'game', 'rating', 'comment']


class CollectionForm(forms.ModelForm):
    """
    Form for creating a collection record.

    This form allows the user to select a user profile, select a game,
    and choose a collection status.
    """

    class Meta:
        """
        Metadata for the CollectionForm model form.
        """
        model = Collection
        fields = ['user_profile', 'game', 'status']