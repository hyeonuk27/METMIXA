<template>
  <div id='Detail'>
    <!-- 배경 -->
    <img id="bg-backdrop" :src="this.selectedMovieInfo.backdrop_path" alt="" :style="{ width: windowWidth }">
    <div id="bg-cover" :style="{ width: windowWidth }"></div>
    <img id="poster" :src="this.selectedMovieInfo.poster_path" rounded alt="" style="width: 300px;">
    <el-progress type="circle" :percentage="vote_average" color="#21d07a" width="60" :stroke-width="5" style="opacity: 0.8;"></el-progress>
    <el-button type="primary" icon="el-icon-edit" circle></el-button>
    <div class="bookmark d-inline-block">
      <i class="fas fa-bookmark" style="font-size: 20px; color: white;"></i>
    </div>
    <div class="d-inline-block">
      <el-rate
        v-model="currentRate"
        :colors="colors"
        @change="giveRate">
      </el-rate>
    </div>
    <div class="container bv-example-row">
      <div id="movieinfo" class="row">
        <div class="col">
          <div id="poster">
          <!-- 가져온 영화 정보 포스터 -->
            
          </div>
          <!-- 별점 주기 -->
          
        </div>
        <!-- 영화정보 -->
        <div>
          <!-- 영화 제목 -->
          <div class="row mb-3">
            <h1 class="text-white">{{ this.selectedMovieInfo.title }}</h1>
          </div>
          <!-- 영화 줄거리 -->
          <div class="row">
            <h3 class="text-white">{{ this.selectedMovieInfo.overview }}</h3>
          </div>
        </div>
      </div>
      <!-- 리뷰 -->
      <div class="row" id="review">
        <!-- 리뷰 작성 -->
        <div class="chat-container" style="background-color: rgba(255, 255, 255, 0.9);">
          <input class="comment-container" v-model="commentText" @keypress.enter="writeComment" placeholder="Enter your opinion" style="background-color: rgba(255, 255, 255, 0);">
        </div>
        <div v-for="(review, idx) in reviews" :key="idx" class="chat-container d-flex align-items-center" style="background-color: rgba(255, 255, 255, 0.9);">
          <img src="https://picsum.photos/1000/1000" alt="Avatar" style="width:100%; margin-left: 10px;">
          <!-- 너무 긴 코멘트가 적힐 경우 짤리지 않도록 처리해줘야한다 -->
          <p class="m-0 text-truncate text-start">{{ review.content }} </p>
          <el-button type="danger" icon="el-icon-delete" circle @click="deleteComment(review.id, idx)" style="margin-left: 110px;"></el-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Detail',
  data: function () {
    return {
      //  별점 주기
      originalRate: '',
      currentRate: '',
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      commentText: '',
      // vuex state로 관리해줘야할듯?
      selectedMovie: '',
      selectedMovieInfo: {},
      reviews: [],
      windowWidth: parseInt(screen.availWidth)+"px",
    }
  },
  methods: {
    writeComment() {
      const content = this.commentText
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config,
        data: {
          content
        }
      })
      // 리뷰 생성 성공
      .then(res => {
        // console.log(this.reviews)
        this.reviews.unshift(res.data)
        this.commentText = ''
      })
      .catch(err => {
        console.log(err)
      })
    },
    // 리뷰 제거
    deleteComment(reviewPk, idx) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/api/v1/reviews/${reviewPk}`,
        headers: this.$store.getters.config,
      })
      // db에서 삭제 후 vue에서 삭제
      .then(res => {
        this.reviews.splice(idx, 1)
        // console.log(this.reviews)
        console.log(res)
      })
      .catch(err => {
        console.log(err)
        alert('권한이 없습니다!')
      })
    },
    // 별점 주기
    giveRate() {
      const rate = this.currentRate
      // 별점을 이미 줬으면 put
      if (this.originalRate) {
        axios({
          method: 'put',
          url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}/rates/`,
          headers: this.$store.getters.config,
          data: {
            rate
          }
        })
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
      // 별점을 주지 않았으면 post
      } else {
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}/rates/`,
          headers: this.$store.getters.config,
          data: {
            rate
          }
        })
        .then(res => {
          console.log(res)
          this.originalRate = res.data.rate
        })
        .catch(err => {
          console.log(err)
        })
      }
    },
  },
  // main page에서 카드를 눌렀을 때 detail page로 이동된 것
  // detail page가 실행되자마자 영화정보, 영화에 대한 리뷰, 유저가 준 rating, 
  // django와 통신은 잘됨
  created() {
    // console.log(this.$store.state.authToken)
    const moviePk = this.$route.query.moviePk
    console.log(moviePk)
    this.selectedMovie = moviePk
    // 영화정보
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}`,
      headers: this.$store.getters.config
    })
    .then(res =>{
      this.selectedMovieInfo = res.data
      // 처음에 가져올 때 리뷰는 따로 저장
      this.reviews = res.data.reviews
    })
    .catch(err => {
      console.log(err)
    })
    // 별점정보
    axios ({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}/rates`,
      headers: this.$store.getters.config
    })
    .then(res => {
      this.originalRate = res.data.rate
      this.currentRate = res.data.rate
    })
    .catch(err => {
      console.log(err)
    })
  },
  computed: {
      vote_average: function () {
        const result = (this.selectedMovieInfo.tmdb_vote_sum + this.selectedMovieInfo.our_vote_sum*2) / (this.selectedMovieInfo.tmdb_vote_cnt + this.selectedMovieInfo.our_vote_cnt)
        return result*10
      }
    }
}
</script>
<style>
#bg-cover {
  position: fixed; 
  z-index: -1;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  margin: auto;
  opacity: 0.9;
  background-color: black;
}
#bg-backdrop {
  position: fixed; 
  z-index: -2;
  top: 0; 
  left: 0; 
  margin: auto;
}
#poster {
  position: absolute;
  top: 10rem;
  left: 30rem; 
}
#bookmark {
  border-radius: 100%;
  display: block;
  width: 10em;
  height: 10em;
  background-color: blue;
}
#Detail {
  background-color: #1414144b;
}
.chat-container {
  border: 2px solid #dedede;
  background-color: #f1f1f1;
  border-radius: 5px;
  padding: 10px;
  margin: 10px 0;
}
.chat-container p {
  width: 80%;
  display: inline-block;
}
.darker {
  border-color: #ccc;
  background-color: #ddd;
}
.chat-container::after {
  content: "";
  clear: both;
  display: table;
}
.chat-container img {
  float: left;
  max-width: 60px;
  width: 100%;
  margin-right: 20px;
  border-radius: 50%;
}
.chat-container img.right {
  float: right;
  margin-left: 20px;
  margin-right:0;
}
.time-right {
  float: right;
  color: #aaa;
}
.time-left {
  float: left;
  color: #999;
}
.comment-container {
  width: 90% !important;
  display: inline !important;
}
</style>