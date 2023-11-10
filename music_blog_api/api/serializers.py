from rest_framework import serializers

from posts.models import Genre, Post, Review, Comment, Playlist


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only = ('rating',)

    def get_rating(self, obj):
        reviews = Review.objects.filter(post=obj.id)
        if reviews:
            total_score = sum(review.score for review in reviews)
            return total_score / len(reviews)
        return 0.0


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=5)
    post = serializers.SlugRelatedField(
        slug_field='id', read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        reaf_only_fields = ('review',)


class PlaylistSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        many=True,
        slug_field='name'
    )

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'posts']
