from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Movie, Review, Genre, Director, Actor
from .serializers import MovieListSerializer, MovieSerializer, ReviewSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import requests
from decouple import config


# 영화 추천 / 조회 리스트 정보
# @api_view(['GET'])
# def index(request):
#     # 추천 알고리즘 작성

#     mode = request.GET.get('mode') # director, actor, title
#     # 조회 1. mode - 최신순, 평점순, 인기순
#     if mode in ('release_date', 'vote_average', 'popularity'):
#         movies = Movie.objects.order_by(f'-{mode}')[:50]
#     elif mode in ('direc')
#     # 조회 2. mode - 감독별, 배우별, 영화명별
#     movies = Movie.objects.filter(mode=request.GET.get('inputValue'))[:50]
#     # 조회 3. 
# ß
#     serializer = MovieListSerializer(movies, many=True)
#     return Response(serializer.data)


# 단일 영화 정보
@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 전체 리뷰 조회, 생성
@api_view(['GET', 'POST'])
def reviews(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 리뷰 detail, 수정, 삭제 + 댓글 생성
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 리뷰 조회
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    # 리뷰 제거
    elif request.method == 'DELETE':
        review.delete()
        data = {
            'delete' : f'{review_pk}번 리뷰가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    # 리뷰 수정
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        # return Response(serializer.data, status=stßatus.HTTP_400_BAD_REQUEST)


# DB 구성
@api_view(['POST'])
def get_movies_db(request):
    # API키는 공개되어서는 안되는 내용이다. .env파일에 넣어두고 decouple을 사용해 꺼내온다.
    API_KEY = config('API_KEY')
    # TMDB의 API를 사용해 한국의 인기있는 영화들을 한국어로 가져온다.
    for page in range(1, 11):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}&region=KR&language=ko'
        # 받아온 json파일을 파이썬에서 활용가능한 dict 타입으로 변환한다.
        req = requests.get(url).json()
        # bulk_create
        Movie.objects.bulk_create(
            # 받아온 데이터에는 results라는 키의 값에 모든 영화의 정보들이 리스트로 담겨있다.
            # 각 영화 정보를 순회하며 이미 영화 제목을 통해 이미 DB에 있는지 확인하고, 없다면 객체를 생성해 DB에 추가되도록 한다.
            [Movie(
                tmdb_id = data.get('id'),
                title = data.get('title'),
                original_title = data.get('original_title'), 
                overview = data.get('overview'), 
                release_date = data.get('release_date'),
                # poster_path는 받아온 데이터에 앞부분 URL을 제외한 이미지의 이름만이 들어있으므로 처리
                poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
                popularity = data.get('popularity'),
                vote_average = data.get('vote_average'),
                backdrop_path = 'https://image.tmdb.org/t/p/w500' + data.get('backdrop_path') if data.get('backdrop_path') else data.get('poster_path'),
                ) for data in req.get('results') if not Movie.objects.filter(title=data.get('title')).exists()]
        )

    return Response({ 'db': '가져왔습니다.' })


@api_view(['POST'])
def get_casts_db(request):
    # API키는 공개되어서는 안되는 내용이다. .env파일에 넣어두고 decouple을 사용해 꺼내온다.
    API_KEY = config('API_KEY')
    movies = get_list_or_404(Movie)
    for movie in movies:
        url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits?api_key={API_KEY}&region=KR&language=ko'
        # 받아온 json파일을 파이썬에서 활용가능한 dict 타입으로 변환한다.
        req = requests.get(url).json()
        # bulk_create
        Director.objects.bulk_create(
            [Director(
                name = data.get('name'),
                original_name = data.get('original_name'),
                ) for data in req.get('crew') if not Director.objects.filter(name=data.get('name')).exists() and data.get('job') == 'Director']
        )

        Actor.objects.bulk_create(
            [Actor(
                name = data.get('name'),
                original_name = data.get('original_name'),
                ) for data in req.get('cast')[:5] if not Actor.objects.filter(name=data.get('name')).exists() and data.get('known_for_department') == 'Acting']
        )

    return Response({ 'db': '가져왔습니다.' })
