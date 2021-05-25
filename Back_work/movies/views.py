from re import L
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Genre, Movie, Review, Comment, Director, Actor, PhotoTicket, Rate, RecommendAlgoScore
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, ReviewSerializer, CommentSerializer, PhotoTicketSerializer, RateSerializer, RecommendAlgoScoreSerializer, DirectorSerializer, ActorSerializer
from django.db.models import F, Q
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import requests
from decouple import config
import random
from django.db.models.aggregates import Sum
from django.core.paginator import Paginator

# 인증된 사용자만 사용할 수 있도록 하는 데코레이터
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


User = get_user_model()

# 메인 페이지
# 영화 추천 / 조회 리스트 정보
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication]) # JWT가 유효한지
@permission_classes([IsAuthenticated]) # 인증 여부를 확인
def movie_list(request):
    mode = request.GET.get('mode')
    # 추천 0. mode - 알고리즘
    # 새로고침 버튼 필요
    if mode == 'algorithm':
        weight = []
        # 장르가 19개 있다.
        for id in range(1, 20):
            genre_weight = RecommendAlgoScore.objects.filter(user__pk=request.user.pk, genre__pk=id).aggregate(Sum('rate'))['rate__sum']
            weight.append(genre_weight if genre_weight else 1)

        recommend_genre_ids = random.choices([28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37], weight, k=6)

        movies = Movie.objects.none()
        for genre_id in recommend_genre_ids:
            temp_movies = Movie.objects.filter(genres__tmdb_genre_id=genre_id)[:25]
            movies = movies|temp_movies

    # 조회 1. mode - 최신순, 평점순, 인기순
    elif mode in ('release_date', 'vote_average', 'popularity'):
        if mode != 'vote_average':
            movies = Movie.objects.order_by(f'-{mode}')[:100]
        else:
            movies = Movie.objects.annotate(vote_average=(F('tmdb_vote_sum') + F('our_vote_sum')) / (F('tmdb_vote_cnt') + F('our_vote_cnt'))).order_by('-vote_average')[:100]
    elif mode in ('director', 'actor', 'title'):
    # 조회 2. mode - 감독별, 배우별, 영화명별
        inputValue = request.GET.get('inputValue')
        if mode == 'director':
            # MtoM 관계에서 원하는 조건을 가지는 영화들을 가져오는 방법
            # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
            movies = Movie.objects.filter(Q(directors__name__icontains=inputValue)|Q(directors__original_name__icontains=inputValue)).distinct()[:100]
        elif mode == 'actor':
            movies = Movie.objects.filter(Q(actors__name__icontains=inputValue)|Q(actors__original_name__icontains=inputValue)).distinct()[:100]
        else:
            # 한글 제목이나 원본 제목이 사용자의 입력(inputValue)를 포함하는 영화들을 반환(대소문자 구분하지 않음)
            movies = Movie.objects.filter(Q(title__icontains=inputValue)|Q(original_title__icontains=inputValue))[:100]
    # 조회 3. mode - 장르별
    elif mode == 'genre':
        inputGenre = request.GET.get('inputGenre')
        movies = Movie.objects.filter(genres__tmdb_genre_id=inputGenre)[:100]

    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 영화 상세 페이지
# 단일 영화 정보
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 감독 정보
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def director(request, movie_pk):
    director = Director.objects.filter(movies__pk=movie_pk).first()
    serializer = DirectorSerializer(director)
    return Response(serializer.data)


# 주연 배우 정보
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def actors(request, movie_pk):
    actors = Actor.objects.filter(movies__pk=movie_pk)[:2]
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)


# 리뷰 조회, 생성
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        reviews = Review.objects.filter(movie__pk=movie_pk).order_by('-pk')
        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page_num')
        reviews = paginator.get_page(page_number)
        serializer = ReviewListSerializer(reviews, many=True)
        data = serializer.data
        data.append({'possible_page': paginator.num_pages})
        return Response(data)
    elif request.method == 'POST':
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 삭제, 수정
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # request.user와 review.user와 같지 않으면 수정 삭제 불가
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.user == review.user:
        # 리뷰 제거
        if request.method == 'DELETE':
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
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 댓글 조회, 생성
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(review__pk=review_pk).order_by('-pk')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Vue에서 axios 요청할 때 URI에 movie의 id값을 넣어서 요청해야 함
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 삭제, 수정
@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        # 댓글 제거
        if request.method == 'DELETE':
            comment.delete()
            data = {
                'delete' : f'{comment_pk}번 댓글이 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        # 댓글 수정
        elif request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 내가 특정 영화에 준 평점 + 유저장르점수 중개테이블 **동시에 두 테이블이 채워지고 업데이트 되는 로직(매직)
# 영화 상세 페이지 로드 시 영화 상세 정보 + 평점 api GET요청 필요
@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def rate(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # filter가 아닌 get으로 가져오면 rate가 하나도 존재하지 않는 시점에서 오류 발생(filter는 객체가 없어도 빈 쿼리셋을 반환) .first()를 통해 하나만 가져온다.
    rate = Rate.objects.filter(user__pk=request.user.pk, movie__pk=movie_pk).first()
    # 함수 내부에서 또 다르게 작동되는 기능: 유저장르점수 중개테이블 채우기
    # 1. movie에 대한 장르 아이디들을 받아온다.
    genres = Genre.objects.filter(movies__pk=movie_pk)
    if request.method == 'GET':
        serializer = RateSerializer(rate)
        return Response(serializer.data)
    # POST를 두 번하게 하면 안된다. Vue에서 if문 분기처리 필요(GET을 하고 인스턴스가 존재하면 PUT, 존재하지 않으면 POST)
    elif request.method == 'POST':
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            # 2. for문을 통해 각 장르 아이디들에 대해서 유저장르점수 객체를 만든다.
            for genre in genres:
                serializer_algo = RecommendAlgoScoreSerializer(data=request.data)
                if serializer_algo.is_valid(raise_exception=True):
                    serializer_algo.save(genre=genre, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        serializer = RateSerializer(rate, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 3. for문을 통해 각 장르 아이디들에 대해 유저장르점수 객체 업데이트
            for genre in genres:
                recommend_algo_score = RecommendAlgoScore.objects.filter(user__pk=request.user.pk, genre__pk=genre.pk).first()
                serializer_algo = RecommendAlgoScoreSerializer(recommend_algo_score, data=request.data)
                if serializer_algo.is_valid(raise_exception=True):
                    serializer_algo.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 포토티켓
# 포토티켓 조회(한 유저에 대한 전체 포토티켓)
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def photo_ticket_list(request):
    photo_tickets = PhotoTicket.objects.filter(user__pk=request.user.pk)
    paginator = Paginator(photo_tickets, 12)
    page_num = request.GET.get('page_num')
    photo_tickets = paginator.get_page(page_num)
    serializer = PhotoTicketSerializer(photo_tickets, many=True)
    data = serializer.data
    data.append({'possible_page': paginator.num_pages})
    return Response(data)


# 포토티켓 단일 조회, 생성(추가), 삭제
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def photo_ticket(request, movie_pk):
    if request.method == 'GET':
        photo_ticket = PhotoTicket.objects.filter(user__pk=request.user.pk, movie__pk=movie_pk).first()
        serializer = PhotoTicketSerializer(photo_ticket)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = PhotoTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie, poster_path=movie.poster_path, title=movie.title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        photo_ticket = PhotoTicket.objects.filter(user__pk=request.user.pk, movie__pk=movie_pk).first()
        photo_ticket.delete()
        data = {
            'delete' : '포토티켓이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


# admin용 api - DB 구성 (장르 - 영화 - 감독, 배우 API 순으로 요청)
# 장르
@api_view(['POST'])
def get_genres_db(request):
    if request.user.username == 'admin':
        # API키는 공개되어서는 안되는 내용이다. .env파일에 넣어두고 decouple을 사용해 꺼내온다.
        API_KEY = config('API_KEY')
        # TMDB의 API를 사용해 한국의 인기있는 영화들을 한국어로 가져온다.
        url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&region=KR&language=ko'
        # 받아온 json파일을 파이썬에서 활용가능한 dict 타입으로 변환한다.
        req = requests.get(url).json()
        Genre.objects.bulk_create(
            [Genre(
                tmdb_genre_id = data.get('id'),
                name = data.get('name'),
                ) for data in req.get('genres')]
        )
        
        return Response({ 'db': '가져왔습니다.' })
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 영화
@api_view(['POST'])
def get_movies_db(request):
    if request.user.username == 'admin':
        API_KEY = config('API_KEY')
        for page in range(1, 11):
            url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}&region=KR&language=ko'
            req = requests.get(url).json()
            for data in req.get('results'):
                # 이미 DB에 있는 영화면 정보를 업데이트
                if Movie.objects.filter(title=data.get('title')).exists():
                    movie = Movie.objects.get(title=data.get('title'))
                    movie.popularity = data.get('popularity')
                    movie.tmdb_vote_sum = data.get('vote_average') * data.get('vote_count')
                    movie.tmdb_vote_cnt = data.get('vote_count')
                    movie.save()
                # DB에 없는 영화면 새로 생성
                else:
                    movie = Movie.objects.create(
                        tmdb_id = data.get('id'),
                        title = data.get('title'),
                        original_title = data.get('original_title'), 
                        release_date = data.get('release_date'),
                        popularity = data.get('popularity'),
                        tmdb_vote_sum = float(data.get('vote_average')) * float(data.get('vote_count')),
                        tmdb_vote_cnt = data.get('vote_count'),
                        our_vote_sum = 0,
                        our_vote_cnt = 0,
                        overview = data.get('overview'),
                        # poster_path는 받아온 데이터에 앞부분 URL을 제외한 이미지의 이름만이 들어있으므로 처리
                        poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
                        backdrop_path = 'https://image.tmdb.org/t/p/w500' + data.get('backdrop_path') if data.get('backdrop_path') else data.get('poster_path'),
                    )
                    for genre_id in data.get('genre_ids'):
                        genre = Genre.objects.get(tmdb_genre_id=genre_id)
                        genre.movies.add(movie)


            # bulk_create의 문제점 -> 통째로 create를 하기 때문에 create된 객체를 받아와 중개모델에 add하는 작업이 불가
            # 따라서, 위 코드처럼 objects 매니저를 사용해 하나하나 객체를 create해주고 반환된 객체를 사용해 중개모델에 add작업을 해준다.

            # bulk_create
            # Movie.objects.bulk_create(
            #     [Movie(
            #         tmdb_id = data.get('id'),
            #         title = data.get('title'),
            #         original_title = data.get('original_title'), 
            #         release_date = data.get('release_date'),
            #         popularity = data.get('popularity'),
            #         tmdb_vote_sum = float(data.get('vote_average')) * float(data.get('vote_count')),
            #         tmdb_vote_cnt = data.get('vote_count'),
            #         our_vote_sum = 0,
            #         our_vote_cnt = 0,
            #         overview = data.get('overview'),
            #         poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
            #         backdrop_path = 'https://image.tmdb.org/t/p/w500' + data.get('backdrop_path') if data.get('backdrop_path') else data.get('poster_path'),
            #         ) for data in req.get('results') if not Movie.objects.filter(title=data.get('title')).exists()]
            # )

        return Response({ 'db': '가져왔습니다.' })
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 감독, 배우
@api_view(['POST'])
def get_casts_db(request):
    if request.user.username == 'admin':
        API_KEY = config('API_KEY')
        movies = get_list_or_404(Movie)
        for movie in movies:
            url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits?api_key={API_KEY}&region=KR&language=ko'
            req = requests.get(url).json()
            for data in req.get('cast')[:5]:
                if not Actor.objects.filter(name=data.get('name')).exists() and data.get('known_for_department') == 'Acting':
                    actor = Actor.objects.create(name=data.get('name'), original_name=data.get('original_name'))
                    actor.movies.add(movie)
            
            for data in req.get('crew'):
                if not Director.objects.filter(name=data.get('name')).exists() and data.get('job') == 'Director':
                    director = Director.objects.create(name=data.get('name'), original_name=data.get('original_name'))
                    director.movies.add(movie)

        return Response({ 'db': '가져왔습니다.' })
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
