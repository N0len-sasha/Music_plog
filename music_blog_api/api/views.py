from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404

from posts.models import Genre, Post, Review
from .serializers import PostSerializer, GenreSerializer, ReviewSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.get_post().reviews.all()

    def update_post_rating(self, post):
        reviews = Review.objects.filter(post=post)
        total_score = sum(review.score for review in reviews)
        new_rating = total_score / reviews.count()

        post.rating = round(new_rating, 2)
        post.save()

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
        post = serializer.instance.post
        self.update_post_rating(post)

    def perform_update(self, serializer):
        serializer.save()
        post = serializer.instance.post
        self.update_post_rating(post)

    def perform_destroy(self, instance):
        post = instance.post
        instance.delete()
        self.update_post_rating(post)
