from django import forms
from posts.models import Post, Genre, Review, Playlist


class PostForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),
                                           label='Жанр',
                                           widget=forms.CheckboxSelectMultiple,
                                           required=True)

    class Meta:
        model = Post
        exclude = ('rating', 'pub_date', 'author')


class ReviewForm(forms.ModelForm):
    score = forms.IntegerField(min_value=1, max_value=5,
                               label='Оценка')

    class Meta:
        model = Review
        fields = ('text', 'score')


class PlayListForm(forms.ModelForm):
    posts = forms.ModelMultipleChoiceField(Post.objects.all(),
                                           widget=forms.CheckboxSelectMultiple)
    image = forms.FileField(required=True)

    class Meta:
        model = Playlist
        fields = ('name', 'image', 'posts')


class AddForm(forms.Form):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.none(),
                                      label='Выберите плейлист')

    def __init__(self, user, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['playlist'].queryset = Playlist.objects.filter(
                author=user)


class PlaylistPostDeleteForm(forms.Form):
    pass
