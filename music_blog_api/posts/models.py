from django.db import models
from django.contrib.auth import get_user_model

from .constants import SLICE_TEXT, MAX_NAME_LENGHT, MAX_DESCTEXT_LENGHT

User = get_user_model()


class BaseModel(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGHT)
    slug = models.SlugField(unique=True)


class Post(BaseModel):
    name = models.CharField(max_length=MAX_NAME_LENGHT)
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/images/',
                              null=True,
                              blank=True)
    audio = models.FileField(upload_to='posts/audio/',
                             null=True,
                             blank=True)
    description = models.TextField(max_length=MAX_DESCTEXT_LENGHT,
                                   null=True,
                                   blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='posts',
    )
    rating = models.FloatField(default=0.0)


class Review(BaseModel):
    text = models.CharField(max_length=MAX_DESCTEXT_LENGHT)
    score = models.PositiveSmallIntegerField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        self.text[:SLICE_TEXT]


class Comment(BaseModel):
    text = models.TextField(max_length=MAX_DESCTEXT_LENGHT)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        self.text[:SLICE_TEXT]

# class Playlist
