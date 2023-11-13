from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg


from .constants import PAGINATION
from .forms import PostForm, ReviewForm
from .mixins import ReviewMixin, PostMixin
from posts.models import Post, Review

'''Pages'''

User = get_user_model()


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = PAGINATION

    def get_queryset(self):
        queryset = Post.objects.annotate(average_rating=Avg('reviews__score'))
        return queryset


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

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user.username})


class DeletePostView(DeleteView):
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


'''Auth'''


class ProfilePageView(ListView):
    template_name = "blog/profile.html"
    context_object_name = "page_obj"
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

    template_name = "registration/registration_form.html"

    form_class = UserCreationForm

    success_url = reverse_lazy("blog:index")
