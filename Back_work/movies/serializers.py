from rest_framework import serializers
from .models import Director, Actor, Movie, Review, Genre, Comment, PhotoTicket, Rate, RecommendAlgoScore
# 실험
from accounts.serializers import UserProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'review', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('review',)


class ReviewListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    # 실험
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'user', 'movie', 'content', 'created_at', 'updated_at', 'comments', 'comments_count')
        read_only_fields = ('movie',)


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'movie', 'content', 'created_at', 'updated_at', 'comments', 'comments_count')
        read_only_fields = ('user', 'movie',)


class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = (
            'id',
            'tmdb_id',
            'title',
            'tmdb_vote_sum', 
            'tmdb_vote_cnt', 
            'our_vote_sum', 
            'our_vote_cnt',
            'poster_path', 
            'backdrop_path',
        )


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    class Meta:
        model = Movie
        fields = (
            'id',
            'tmdb_id', 
            'title',
            'original_title',
            'release_date',
            'popularity',
            'tmdb_vote_sum', 
            'tmdb_vote_cnt', 
            'our_vote_sum', 
            'our_vote_cnt',
            'overview', 
            'poster_path', 
            'backdrop_path', 
            'genres', 
            'reviews', 
            'reviews_count'
        )


# 필수사항이 아님. 여력이 있으면 하기
class GenreSerializer(serializers.ModelSerializer):
    pass


class PhotoTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoTicket
        fields = ('id', 'user', 'movie', 'title', 'poster_path',)
        read_only_fields = ('user', 'movie', 'poster_path', 'title',)


class RateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rate
        fields = ('id', 'user', 'movie', 'rate',)
        read_only_fields = ('user', 'movie',)


class RecommendAlgoScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommendAlgoScore
        fields = ('id', 'user', 'genre', 'rate',)
        read_only_fields = ('user', 'genre',)


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ('id', 'name',)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ('id', 'name',)