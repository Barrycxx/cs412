"""
mini_insta/views.py
Xinxu Chen (chenxin@bu.edu)

Views for mini_insta.
"""
from django.db import models
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import render

from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdatePostForm, UpdateProfileForm


class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context


class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs["pk"])

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        # Task 1: uploaded files (multiple)
        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=post, image_file=f)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})


# ---------------- Task 3: Delete / Update Post ----------------

class DeletePostView(DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.object.profile.pk})


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})


# ---------------- Task 2: Update Profile ----------------

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"


# ---------------- Task 4: Show followers / following ----------------

class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


# ---------------- Task 5: Feed ----------------

class PostFeedListView(ListView):
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context


# ---------------- Task 6: Search ----------------

class SearchView(ListView):
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        if "query" not in self.request.GET:
            profile = Profile.objects.get(pk=self.kwargs["pk"])
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get("query", "").strip()
        if q == "":
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=q).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        q = self.request.GET.get("query", "").strip()

        context["profile"] = profile
        context["query"] = q
        context["posts"] = self.get_queryset()

        if q == "":
            context["profiles"] = Profile.objects.none()
        else:
            context["profiles"] = Profile.objects.filter(
                models.Q(username__icontains=q) |
                models.Q(display_name__icontains=q) |
                models.Q(bio_text__icontains=q)
            ).order_by("username")

        return context