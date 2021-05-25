<template>
  <div id='Detail'>
    <!-- 배경 -->
    <img id="bg-backdrop" :src="this.selectedMovieInfo.backdrop_path" alt="" :style="{ width: windowWidth }">
    <div id="bg-cover" :style="{ width: windowWidth }"></div>
    <img id="poster" :src="this.selectedMovieInfo.poster_path" rounded alt="" style="width: 300px; border-radius: 7px;">
    
    <div id="info-div">
      <h1 id="movie-title" class="text-white text-start">{{ this.selectedMovieInfo.title }}</h1>
      <div class="d-flex justify-content-start mt-4 mb-4">
      <div class="d-inline-block">
        <span class="text-white me-2">평점</span>
        <h5 id="percentage">{{ vote_average }}<span style="font-size: 6px;">%</span></h5>
        <el-progress 
          type="circle"
          v-if="vote_average"
          :percentage="vote_average"
          color="#21d07a"
          :width=60
          :stroke-width="5"
          :show-text="false"
          style="opacity: 0.8;"
          >
          </el-progress>
      </div>
      <div class="d-inline-block d-flex align-items-center ms-3">
        <el-rate
          v-model="currentRate"
          :colors="colors"
          @change="giveRate"
          >
        </el-rate>
        <el-tooltip :content="tooltip" placement="right">
          <v-btn v-if="!isPhototicket" icon id="add-photo-ticket-icon" @click="addMyPhototicket" @mousedown="$vs.notify({title:'포토티켓 추가!',text:'이제 내 프로필에서 언제든 확인할 수 있어요', color:'danger', icon:'favorite'})" class="ms-2">
            <v-icon>mdi-heart</v-icon>
          </v-btn>
          <v-btn v-else icon id="remove-photo-ticket-icon" @click="removeMyPhototicket" @mousedown="$vs.notify({title:'포토티켓 삭제...',text:'다시 한 번 눌러주실거죠? 😥', color:'dark', icon:'delete'})" class="ms-2">
            <v-icon>mdi-heart</v-icon>
          </v-btn>
        </el-tooltip>
      </div>
      </div>
      <p id="movie-overview" class="text-white text-start">{{ this.selectedMovieInfo.overview }}</p>
      <div id="movie-casts" class="text-white d-flex row mt-4 text-start">
        <h6 class="col-4">감독</h6>
        <h6 class="col-4">주연 배우</h6>
        <h6 class="col-4">주연 배우</h6>
      </div>
      <div id="movie-casts" class="text-white d-flex row text-start">
        <h6 class="col-4">{{ director }}</h6>
        <h6 class="col-4">{{ actors[0] }}</h6>
        <h6 class="col-4">{{ actors[1] }}</h6>
      </div>
    </div>
    <div id="comment">
      <div style="width: 100%; height: 100px; background-color: rgb(231, 231, 230); border-radius: 5px;">
        {{ selectedReviewInfo.content }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'
import { mapState } from 'vuex'

export default {
  name: 'Comment',
  data: function () {
    return {
      originalRate: '',
      currentRate: 1,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      selectedMovie: '',
      selectedMovieInfo: {},
      selectedReview: '',
      selectedReviewInfo: {},
      commentText: '',
      comments: [],
      windowWidth: parseInt(screen.availWidth)+"px",
      isPhototicket: false,
      tooltip: '',
      director: '',
      actors: [],
      pageNum: 1,
      possiblePageNum: 2,
      SERVER_URL: SERVER.URL,
      review: {},
    }
  },
  methods: {
    giveRate: function () {
      const rate = this.currentRate
      this.$vs.notify({title:'평점 후원!',text: `${this.nickname}님! ${this.currentRate}점 후원 감사합니다! 😘`,color:'warning',icon:'star'})
      // 별점을 이미 줬으면 put
      if (this.originalRate) {
        axios({
          method: 'put',
          url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates/`,
          headers: this.$store.getters.config,
          data: {
            rate: rate*20,
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
          url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates/`,
          headers: this.$store.getters.config,
          data: {
            rate: rate*20,
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
    // 내 포토티켓에 등록하기
    addMyPhototicket: function () {
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/phototickets/`,
        headers: this.$store.getters.config,
      })
      .then(() => {
        this.isPhototicket = true
        this.tooltip = '포토티켓 삭제'
      })
      .catch(err => {
        console.log(err)
      })
    },
    // 포토티켓에서 삭제하기
    removeMyPhototicket: function () {
      axios({
        method: 'delete',
        url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/phototickets/`,
        headers: this.$store.getters.config,
      })
      .then(() => {
        this.isPhototicket = false
        this.tooltip = '포토티켓 담기'
      })
      .catch(err => {
        console.log(err)
      })
    },
    humanize: function (date) {
      const moment = require('moment')
      const created = moment(date).format('YYYY-MM-DD')
      return created
    }
  },
  // main page에서 카드를 눌렀을 때 detail page로 이동된 것
  // detail page가 실행되자마자 영화정보, 영화에 대한 리뷰, 유저가 준 rating, 
  // django와 통신은 잘됨
  created() {
    const moviePk = this.$route.query.movie
    this.selectedMovie = moviePk
    // 영화정보
    axios({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}`,
      headers: this.$store.getters.config
    })
    .then(res =>{
      this.selectedMovieInfo = res.data
    })
    .catch(err => {
      console.log(err)
    })
    // 리뷰정보
    const reviewPk = this.$route.query.review
    this.selectedReview = reviewPk
    axios({
      method: 'get',
      url: `${SERVER.URL}/api/v1/reviews/${this.selectedReview}`,
      headers: this.$store.getters.config
    })
    .then(res =>{
      this.selectedReviewInfo = res.data
    })
    .catch(err => {
      console.log(err)
    })
    // 별점정보
    axios ({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates`,
      headers: this.$store.getters.config
    })
    .then(res => {
      this.originalRate = res.data.rate
      this.currentRate = res.data.rate
    })
    .catch(err => {
      console.log(err)
    }),
    // 포토티켓 여부
    axios ({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/phototickets/`,
      headers: this.$store.getters.config
    })
    .then(res => {
      if (Object.keys(res.data).length) {
        this.isPhototicket = true
        this.tooltip = '포토티켓 삭제'
      } else {
        this.isPhototicket = false
        this.tooltip = '포토티켓 담기'
      }
    })
    .catch(err => {
      console.log(err)
    })
    // 감독 정보
    axios ({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/director/`,
      headers: this.$store.getters.config
    })
    .then(res => {
      this.director = res.data.name
    })
    .catch(err => {
      console.log(err)
    }),
    // 배우 정보
    axios ({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/actors/`,
      headers: this.$store.getters.config
    })
    .then(res => {
      res.data.forEach(actor => {
        this.actors.push(actor.name)
      });
    })
    .catch(err => {
      console.log(err)
    }),
    this.getReviews()
    document.addEventListener('scroll', this.checkBottom)
  },
  computed: {
    vote_average: function () {
      const result = ((this.selectedMovieInfo.tmdb_vote_sum + this.selectedMovieInfo.our_vote_sum*2) / (this.selectedMovieInfo.tmdb_vote_cnt + this.selectedMovieInfo.our_vote_cnt)).toFixed(1)
      return result*10
    },
    ...mapState([
      'nickname',
      'image',
    ])
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
#comment{
  position: absolute;
  top: 35rem;
  left: 23.5rem;
  width: 70rem;
}
</style>