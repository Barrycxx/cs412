"""
mini_insta/views.py
Xinxu Chen (chenxin@bu.edu)

Views for mini_insta.
"""

from django.db import models
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .serializers import ProfileSerializer, PostSerializer, CreatePostSerializer
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdatePostForm, UpdateProfileForm, CreateProfileForm


class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("mini_insta:login")

    def get_login_url(self):
        return str(self.login_url)

    def get_logged_in_profile(self):
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile is None:
            raise Http404("No profile found for this user.")
        return profile


class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            context["logged_in_profile"] = logged_in_profile
            context["is_own_profile"] = (logged_in_profile == self.object)
            if logged_in_profile:
                context["already_following"] = logged_in_profile.is_following(self.object)
            else:
                context["already_following"] = False
        else:
            context["logged_in_profile"] = None
            context["is_own_profile"] = False
            context["already_following"] = False

        return context


class MyProfileDetailView(MiniInstaLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.get_logged_in_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged_in_profile"] = self.object
        context["is_own_profile"] = True
        context["already_following"] = False
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile

        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            context["logged_in_profile"] = logged_in_profile
            if logged_in_profile:
                context["already_liked"] = self.object.is_liked_by(logged_in_profile)
                context["is_own_post"] = (self.object.profile == logged_in_profile)
            else:
                context["already_liked"] = False
                context["is_own_post"] = False
        else:
            context["logged_in_profile"] = None
            context["already_liked"] = False
            context["is_own_post"] = False

        return context


class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_logged_in_profile()
        return context

    def form_valid(self, form):
        profile = self.get_logged_in_profile()

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=post, image_file=f)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})


class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        logged_in_profile = self.get_logged_in_profile()

        if self.object.profile != logged_in_profile:
            return redirect("mini_insta:show_post", pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.object.profile.pk})


class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        logged_in_profile = self.get_logged_in_profile()

        if self.object.profile != logged_in_profile:
            return redirect("mini_insta:show_post", pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})


class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.get_logged_in_profile()


class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_logged_in_profile()
        context["profile"] = profile
        context["logged_in_profile"] = profile

        liked_posts = Like.objects.filter(profile=profile)
        context["liked_post_ids"] = [like.post.pk for like in liked_posts]

        return context


class SearchView(MiniInstaLoginRequiredMixin, ListView):
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_logged_in_profile()

        if "query" not in self.request.GET:
            return render(request, "mini_insta/search.html", {"profile": profile})

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get("query", "").strip()

        if q == "":
            return Post.objects.none()

        return Post.objects.filter(caption__icontains=q).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_logged_in_profile()
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


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "user_form" not in context:
            context["user_form"] = UserCreationForm()

        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        user = user_form.save()

        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        form.instance.user = user
        form.instance.username = user.username
        form.instance.join_date = timezone.now().date()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mini_insta:profile")


class FollowProfileView(MiniInstaLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_profile = self.get_logged_in_profile()
        other_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])

        if logged_in_profile != other_profile:
            Follow.objects.get_or_create(
                profile=other_profile,
                follower_profile=logged_in_profile
            )

        return redirect("mini_insta:show_profile", pk=other_profile.pk)


class DeleteFollowProfileView(MiniInstaLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_profile = self.get_logged_in_profile()
        other_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])

        Follow.objects.filter(
            profile=other_profile,
            follower_profile=logged_in_profile
        ).delete()

        return redirect("mini_insta:show_profile", pk=other_profile.pk)


class LikePostView(MiniInstaLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_profile = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        if post.profile != logged_in_profile:
            Like.objects.get_or_create(post=post, profile=logged_in_profile)

        return redirect("mini_insta:show_post", pk=post.pk)


class DeleteLikePostView(MiniInstaLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_profile = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        Like.objects.filter(post=post, profile=logged_in_profile).delete()

        return redirect("mini_insta:show_post", pk=post.pk)


class LogoutConfirmationView(TemplateView):
    template_name = "mini_insta/logged_out.html"


class APILoginView(APIView):
    """
    Handles API login and returns an auth token plus the profile id.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")

        if username == "" or password == "":
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = Profile.objects.filter(user=user).first()

        if profile is None:
            return Response(
                {"error": "No profile found for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "profile_id": profile.pk,
                "username": profile.username,
                "display_name": profile.display_name,
            },
            status=status.HTTP_200_OK
        )


class AuthenticatedProfileAPIMixin:
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_authenticated_profile(self):
        profile = Profile.objects.filter(user=self.request.user).first()

        if profile is None:
            raise PermissionDenied("No profile found for this user.")

        return profile

    def get_requested_profile(self):
        profile = self.get_authenticated_profile()

        if int(self.kwargs["pk"]) != profile.pk:
            raise PermissionDenied("You can only access your own profile data.")

        return profile


class APIProfileListView(generics.ListAPIView):
    """
    Returns all profiles for an authenticated user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all().order_by("username")
    serializer_class = ProfileSerializer


class APIProfileDetailView(AuthenticatedProfileAPIMixin, generics.RetrieveAPIView):
    """
    Returns one profile by id.
    """
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.get_requested_profile()


class APIProfilePostsView(AuthenticatedProfileAPIMixin, generics.ListAPIView):
    """
    Returns all posts for one profile.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        profile = self.get_requested_profile()
        return profile.get_all_posts()


class APIProfileFeedView(AuthenticatedProfileAPIMixin, generics.ListAPIView):
    """
    Returns the feed for one profile.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        profile = self.get_requested_profile()
        return profile.get_post_feed()


class APICreatePostView(AuthenticatedProfileAPIMixin, generics.CreateAPIView):
    """
    Creates a post for one profile.
    """
    serializer_class = CreatePostSerializer

    def create(self, request, *args, **kwargs):
        profile = self.get_requested_profile()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            post = Post.objects.create(
                profile=profile,
                caption=serializer.validated_data.get("caption", "")
            )
            output_serializer = PostSerializer(post)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)