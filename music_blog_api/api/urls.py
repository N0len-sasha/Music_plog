from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, GenreViewSet, ReviewViewSet

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [

    path('v1/genres/', GenreViewSet.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
