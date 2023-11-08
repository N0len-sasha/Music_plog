from django.contrib import admin
from .models import Playlist, Post, Genre, Review, Comment


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pub_date', 'rating')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'score', 'post']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'review']


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
