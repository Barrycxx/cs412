"""
mini_insta/views.py
Xinxu Chen (chenxin@bu.edu)

Views for mini_insta.
"""

from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Profile, Post, Photo
from .forms import CreatePostForm


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

        image_url = self.request.POST.get("image_url", "").strip()
        if image_url != "":
            Photo.objects.create(post=post, image_url=image_url)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})