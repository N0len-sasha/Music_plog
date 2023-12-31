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

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Post(BaseModel):
    name = models.CharField(max_length=MAX_NAME_LENGHT,
                            unique=True,
                            verbose_name='Название песни')
    image = models.ImageField(upload_to='images/',
                              null=True,
                              blank=True,
                              verbose_name='Изображение(обложка)')
    audio = models.FileField(upload_to='audio/',
                             null=True,
                             blank=True,
                             verbose_name='Аудио файл(mp3)')
    description = models.TextField(max_length=MAX_DESCTEXT_LENGHT,
                                   null=True,
                                   blank=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='posts',
        verbose_name='Жанр'
    )
    rating = models.FloatField(default=0.0)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.name


class Review(BaseModel):
    text = models.CharField(max_length=MAX_DESCTEXT_LENGHT,
                            verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:SLICE_TEXT]


class Playlist(BaseModel):
    name = models.CharField(max_length=MAX_NAME_LENGHT,
                            verbose_name='Название плейлиста')
    image = models.ImageField(upload_to='images/',
                              null=True,
                              blank=True,
                              verbose_name='Обложка плейлиста')
    posts = models.ManyToManyField(
        Post,
        through='PlaylistPost',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'

    def __str__(self):
        return self.name[:MAX_NAME_LENGHT]


class PlaylistPost(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь плейлиста и поста'
        verbose_name_plural = 'Связи плейлистов и постов'
