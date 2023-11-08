from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (PostViewSet,
                    GenreViewSet,
                    ReviewViewSet,
                    CommentViewSet,
                    PlaylistViewSet)

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'posts/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'playlists', PlaylistViewSet, basename='playlists'
)

urlpatterns = [

    path('v1/genres/', GenreViewSet.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
