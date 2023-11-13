from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.shortcuts import redirect


from posts.models import Review, Post
from .forms import ReviewForm, PostForm


class AuthorCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class ReviewMixin(LoginRequiredMixin):
    model = Review
    form_class = ReviewForm
    template_name = 'blog/review.html'
    pk_url_kwarg = 'review_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostMixin(AuthorCheckMixin, LoginRequiredMixin):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.get_object().id)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
