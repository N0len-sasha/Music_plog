from django.contrib import admin
from .models import Playlist, Post, Genre, Review


# class PostItemTabular(admin.TabularInline):
#     model = Post


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')

    # inlines = [
    #     PostItemTabular,
    # ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pub_date', 'rating', 'display_genres')
    filter_horizontal = ('genre',)

    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    display_genres.short_description = 'Genres'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'score', 'post']