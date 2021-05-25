from django.contrib import admin
from .models import Movie, Review, Genre, Comment, Director, Actor, PhotoTicket, Rate, RecommendAlgoScore


class MovieAdmin(admin.ModelAdmin):
    list_display = ['tmdb_id', 'title', 'original_title', 'release_date', 'popularity', 'tmdb_vote_sum', 'tmdb_vote_cnt', 'our_vote_sum', 'our_vote_cnt', 'overview', 'poster_path', 'backdrop_path']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['tmdb_genre_id', 'name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'review' , 'content' , 'created_at', 'updated_at']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'content', 'created_at', 'updated_at']


class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_name']


class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_name']


class PhotoTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'title', 'poster_path']


class RateAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rate']


class RecommendAlgoScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'genre']

    
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(PhotoTicket, PhotoTicketAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(RecommendAlgoScore, RecommendAlgoScoreAdmin)