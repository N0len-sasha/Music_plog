from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Post(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    audio = models.FileField(upload_to='posts/audio/', null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='posts',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    # rating =
