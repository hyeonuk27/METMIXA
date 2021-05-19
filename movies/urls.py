from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path('<int:movie_pk>/', views.detail),
    # path('reviews/', views.reviews),
    # path('reviews/<int:review_pk>/', views.review),
    path('db/movies/', views.get_movies_db),
    path('db/casts/', views.get_casts_db),
]