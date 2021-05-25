from django.db import models
from django.conf import settings
from django.db.models.fields import FloatField

User = settings.AUTH_USER_MODEL

# 장르
class Genre(models.Model):
    tmdb_genre_id = models.IntegerField()
    name = models.CharField(max_length=50)


# 영화
class Movie(models.Model): # 총 13개 필드
    genres = models.ManyToManyField(Genre, related_name='movies')
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    tmdb_vote_sum = models.FloatField()
    tmdb_vote_cnt = models.IntegerField()
    our_vote_sum = models.IntegerField()
    our_vote_cnt = models.IntegerField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    # 커스텀한 중개 테이블을 사용하지 않는다면 사용
    # bookmark_users = models.ManyToManyField(User, related_name='my_movies')


# 리뷰
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    nickname = models.CharField(max_length=50)
    image_url = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 감독
class Director(models.Model):
    movies = models.ManyToManyField(Movie, related_name='directors')
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100)


# 배우
class Actor(models.Model):
    movies = models.ManyToManyField(Movie, related_name='actors')
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100)


# 포토티켓
class PhotoTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookmark_users')
    title = models.CharField(max_length=100)
    poster_path = models.TextField()


# 평점 -> 영화 상세 페이지에서 내가 남겨줄려고
class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_rate')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_rate')
    rate = models.FloatField()


# 유저_장르_점수
class RecommendAlgoScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_score')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='user_score')
    rate = models.FloatField()