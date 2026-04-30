"""
project/views.py
Xinxu Chen (chenxin@bu.edu)

Views for the final project app. These views display lists and details
for the models in the video game collection and review tracker, and
also support basic CRUD operations and game searching.
"""

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import UserProfile, Genre, Game, Review, Collection
from .forms import ReviewForm, CollectionForm


class GenreListView(ListView):
    """
    Display a list of all genres.
    """
    model = Genre
    template_name = 'project/genre_list.html'
    context_object_name = 'genres'


class GenreDetailView(DetailView):
    """
    Display the details for one genre.

    Parameters:
        pk: The primary key of the genre to display.
    """
    model = Genre
    template_name = 'project/genre_detail.html'
    context_object_name = 'genre'


class GameListView(ListView):
    """
    Display a list of all games and allow simple searching/filtering.
    """
    model = Game
    template_name = 'project/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        """
        Return the filtered list of games.

        The queryset may be filtered by:
        - q: a search term for title or developer
        - platform: a platform name
        - genre: a genre name
        """
        queryset = Game.objects.all()

        query = self.request.GET.get('q')
        platform = self.request.GET.get('platform')
        genre = self.request.GET.get('genre')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(developer__icontains=query)
            )

        if platform:
            queryset = queryset.filter(platform__icontains=platform)

        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Return the template context for the game list page.

        Parameters:
            **kwargs: Additional keyword arguments passed to the parent
                context method.

        The returned context includes the current search and filter values
        so they can be displayed again in the form.
        """
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['platform'] = self.request.GET.get('platform', '')
        context['genre_search'] = self.request.GET.get('genre', '')
        return context


class GameDetailView(DetailView):
    """
    Display the details for one game.

    Parameters:
        pk: The primary key of the game to display.
    """
    model = Game
    template_name = 'project/game_detail.html'
    context_object_name = 'game'


class UserProfileListView(ListView):
    """
    Display a list of all user profiles.
    """
    model = UserProfile
    template_name = 'project/userprofile_list.html'
    context_object_name = 'profiles'


class UserProfileDetailView(DetailView):
    """
    Display the details for one user profile.

    Parameters:
        pk: The primary key of the user profile to display.
    """
    model = UserProfile
    template_name = 'project/userprofile_detail.html'
    context_object_name = 'profile'


class ReviewListView(ListView):
    """
    Display a list of all reviews.
    """
    model = Review
    template_name = 'project/review_list.html'
    context_object_name = 'reviews'


class ReviewDetailView(DetailView):
    """
    Display the details for one review.

    Parameters:
        pk: The primary key of the review to display.
    """
    model = Review
    template_name = 'project/review_detail.html'
    context_object_name = 'review'


class ReviewCreateView(CreateView):
    """
    Create a new review using ReviewForm.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'project/review_form.html'
    success_url = reverse_lazy('project:review_list')


class ReviewUpdateView(UpdateView):
    """
    Update an existing review using ReviewForm.

    Parameters:
        pk: The primary key of the review to update.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'project/review_form.html'
    success_url = reverse_lazy('project:review_list')


class ReviewDeleteView(DeleteView):
    """
    Delete an existing review.

    Parameters:
        pk: The primary key of the review to delete.
    """
    model = Review
    template_name = 'project/review_confirm_delete.html'
    success_url = reverse_lazy('project:review_list')


class CollectionListView(ListView):
    """
    Display a list of all collection records.
    """
    model = Collection
    template_name = 'project/collection_list.html'
    context_object_name = 'collections'


class CollectionDetailView(DetailView):
    """
    Display the details for one collection record.

    Parameters:
        pk: The primary key of the collection record to display.
    """
    model = Collection
    template_name = 'project/collection_detail.html'
    context_object_name = 'collection'


class CollectionCreateView(CreateView):
    """
    Create a new collection record using CollectionForm.
    """
    model = Collection
    form_class = CollectionForm
    template_name = 'project/collection_form.html'
    success_url = reverse_lazy('project:collection_list')