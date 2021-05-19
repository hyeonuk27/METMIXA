from django.db import models
from django.conf import settings
from django.db.models.fields import FloatField

User = settings.AUTH_USER_MODEL
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    recommend_users = models.ManyToManyField(User, related_name='recommend_genres')


class Movie(models.Model):
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    genres = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(User, related_name='like_movies')
    dislike_users = models.ManyToManyField(User, related_name='dislike_movies')
    bookmark_users = models.ManyToManyField(User, related_name='my_movies')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Director(models.Model):
    movies = models.ManyToManyField(Movie, related_name='directors')
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100)


class Actor(models.Model):
    movies = models.ManyToManyField(Movie, related_name='actors')
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100)