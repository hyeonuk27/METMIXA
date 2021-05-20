from rest_framework import serializers
from .models import Movie, Review, Genre


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ('user', 'movie', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('movie', 'user',)


class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = (
            'tmdb_id',
            'title',
            'tmdb_vote_sum', 
            'tmdb_vote_cnt', 
            'our_vote_sum', 
            'our_vote_cnt',
            'poster_path', 
        )


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    class Meta:
        model = Movie
        fields = (
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


class GenreSerializer(serializers.ModelSerializer):
    pass