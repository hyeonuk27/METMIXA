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
       fields = ('title', 'poster_path', 'tmdb_id',)


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)
    class Meta:
        model = Movie
        fiedls = ('tmdb_id', 'title', 'overview', 'release_date', 'poster_path', 'backdrop_path', 'popularity', 'vote_average', 'genres', 'reviews', 'reviews_count')


class GenreSerializer(serializers.ModelSerializer):
    pass