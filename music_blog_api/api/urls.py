from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, GenreViewSet

router = SimpleRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [

    path('v1/genres/', GenreViewSet.as_view()),
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
