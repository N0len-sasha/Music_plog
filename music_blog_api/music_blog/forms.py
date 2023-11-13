from django import forms
from posts.models import Post, Genre, Review


class PostForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),
                                           label='Жанр',
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False)

    class Meta:
        model = Post
        exclude = ('rating', 'pub_date', 'author')


class ReviewForm(forms.ModelForm):
    score = forms.IntegerField(min_value=1, max_value=5,
                               label='Оценка')

    class Meta:
        model = Review
        fields = ('text', 'score')
