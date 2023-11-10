from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from posts.models import Post
from .constants import PAGINATION

'''Pages'''


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "page_obj"
    paginate_by = PAGINATION

    def get_queryset(self):
        return Post.objects.all()


class AboutPageView(TemplateView):
    template_name = 'blog/about.html'


'''Posts'''


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = 'post'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return post


'''Auth'''


class ProfilePageView(TemplateView):
    template_name = 'blog/profile.html'
