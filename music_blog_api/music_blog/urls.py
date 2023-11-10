from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'),
    path('about/',
         views.AboutPageView.as_view(),
         name='about'),
    path('profile/',
         views.ProfilePageView.as_view(),
         name='profile'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail')
]