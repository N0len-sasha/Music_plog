from django.views.generic import ListView

from posts.models import Post
from django.views.generic import TemplateView


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "page_obj"

    def get_queryset(self):
        return Post.objects.all()


class AboutPageView(TemplateView):
    template_name = 'blog/about.html'

class ProfilePageView(TemplateView):
    template_name = 'blog/profile.html'
