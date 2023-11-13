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
    path('profile/<str:username>/',
         views.ProfilePageView.as_view(),
         name='profile'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/',
         views.CreatePostView.as_view(),
         name='post_create'),
    path('posts/<int:post_id>/review/',
         views.AddReviewView.as_view(),
         name='add_review'),
    path('posts/<int:post_id>/delete/',
         views.DeletePostView.as_view(),
         name='post_delete'),
    path('posts/<int:post_id>/edit/',
         views.EditPostView.as_view(),
         name='edit_post'),
]
