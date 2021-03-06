from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/phototickets/', views.photo_ticket),
    path('movies/<int:movie_pk>/reviews/', views.review_list),
    path('movies/<int:movie_pk>/rates/', views.rate),
    path('movies/<int:movie_pk>/director/', views.director),
    path('movies/<int:movie_pk>/actors/', views.actors),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('phototickets/', views.photo_ticket_list),
    path('db/genres/', views.get_genres_db),
    path('db/movies/', views.get_movies_db),
    path('db/casts/', views.get_casts_db),
]