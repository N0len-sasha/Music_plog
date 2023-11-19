from typing import Any
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView, CreateView,
                                  DeleteView, UpdateView,
                                  FormView)
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count


from .constants import PAGINATION
from .forms import (PostForm, ReviewForm, EditProfileForm,
                    PlayListForm, AddForm, PlaylistPostDeleteForm)
from .mixins import ReviewMixin, PostMixin, AuthorCheckMixin
from posts.models import Post, Review, Playlist

'''Pages'''

User = get_user_model()


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = Post.objects.annotate(average_rating=Avg('reviews__score'))
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        return queryset.order_by('-average_rating')


class AboutPageView(TemplateView):
    template_name = 'blog/about.html'


'''Posts'''


class PostDetailView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "blog/detail.html"
    context_object_name = "reviews"
    paginate_by = PAGINATION

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return post

    def get_queryset(self):
        return self.get_object().reviews.select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        average_score = Review.objects.filter(
            post=post).aggregate(Avg('score'))['score__avg']
        context["form"] = ReviewForm()
        context["post"] = self.get_object()
        context["average_score"] = average_score
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user.username})


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:index")
    template_name = 'blog/post_confirm_delete.html'
    pk_url_kwarg = 'post_id'


class EditPostView(PostMixin, UpdateView):
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class AddReviewView(ReviewMixin, CreateView):
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewDeleteView(ReviewMixin, AuthorCheckMixin, DeleteView):
    pass


class ReviewUpdateView(ReviewMixin, AuthorCheckMixin, UpdateView):
    pass


'''Auth'''


class ProfilePageView(ListView):
    template_name = "blog/profile.html"
    paginate_by = PAGINATION

    def get_profile(self):
        return get_object_or_404(get_user_model(),
                                 username=self.kwargs["username"])

    def get_queryset(self):
        author = self.get_profile()
        queryset = Post.objects.filter(author=author).annotate(
            average_rating=Avg('reviews__score'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        return context


class RegistrationView(CreateView):

    template_name = 'registration/registration_form.html'

    form_class = UserCreationForm

    success_url = reverse_lazy("blog:index")


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EditProfileForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user.username})


'''Playlists'''


class PlayListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'blog/playlist.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        author = self.request.user
        queryset = Playlist.objects.filter(author=author).annotate(
            post_count=Count('posts')
        )
        return queryset


class AddToPlaylistView(LoginRequiredMixin, FormView):
    template_name = 'blog/add_to_playlist.html'
    form_class = AddForm

    def get_success_url(self):
        return reverse('blog:index')

    def get_form_kwargs(self):
        kwargs = super(AddToPlaylistView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        playlist_id = form.cleaned_data['playlist'].id

        post = get_object_or_404(Post, pk=post_id)
        playlist = get_object_or_404(Playlist, pk=playlist_id)

        playlist.posts.add(post)

        return super().form_valid(form)


class CreatePlayListView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlayListForm
    template_name = 'blog/playlist_create.html'

    def get_success_url(self):
        return reverse('blog:playlists')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        return super().form_valid(form)


class PlayListDetailView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/playlist_detail.html'
    context_object_name = 'posts'

    def get_object(self):
        playlist = get_object_or_404(Playlist, pk=self.kwargs["playlist_id"])
        return playlist

    def get_queryset(self):
        queryset = self.get_object().posts.all()
        return queryset

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()
        context['playlist'] = playlist
        return context


class DeletePlaylistView(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = reverse_lazy("blog:playlists")
    template_name = 'blog/playlist_confirm_delete.html'
    pk_url_kwarg = 'playlist_id'


class PostDisableView(FormView):
    template_name = 'blog/playlist_post_delete.html'
    form_class = PlaylistPostDeleteForm

    def get_success_url(self):
        return reverse('blog:playlist_detail',
                       kwargs={'playlist_id': self.kwargs['playlist_id']})

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['playlist'] = get_object_or_404(Playlist,
                                                pk=self.kwargs["playlist_id"])
        context['post'] = get_object_or_404(Post,
                                            pk=self.kwargs["post_id"])
        return context

    def post(self, request, *args, **kwargs):
        playlist_id = self.kwargs['playlist_id']
        post_id = self.kwargs['post_id']

        playlist = get_object_or_404(Playlist, id=playlist_id)
        post = get_object_or_404(Post, id=post_id)

        playlist.posts.remove(post)

        return self.form_valid(self.get_form())
