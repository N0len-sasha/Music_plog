from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404

from posts.models import Genre, Post, Playlist
from .serializers import (PostSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          PlaylistSerializer)


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

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        return Playlist.objects.filter(id=playlist_id)
