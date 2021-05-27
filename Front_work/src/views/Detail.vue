<template>
  <div id='Detail'>
    <!-- 배경 -->
    <h1 id='logo' @click="$router.push({ name: 'Main' })">MET<span style="color: rgba(140, 100, 172, 0.8);">MIX</span>A</h1>
    <img id="bg-backdrop" :src="this.selectedMovieInfo.backdrop_path" alt="" :style="{ width: windowWidth }">
    <div id="bg-cover" :style="{ width: windowWidth }"></div>
    <img id="poster" :src="this.selectedMovieInfo.poster_path" rounded alt="" style="width: 300px; border-radius: 7px;">
    <div id="sideText">
      <h1 style="margin-bottom: 2vh; color: rgba(140, 100, 172, 0.8); font-size: 3.2vh; font-family: 'Nanum Myeongjo', serif;">MIX</h1>
      <p style="width: 20vh; font-size: 1.65vh;">같은 취향을 가진 사람들과</p>
      <p style="width: 20vh; font-size: 1.65vh;">영화에 대한 감상을 나누며</p>
      <p style="width: 20vh; font-size: 1.65vh;">생각을 섞는 공간</p>
    </div>
    
    <div id="info-div">
      <h1 id="movie-title" class="text-white text-start">{{ this.selectedMovieInfo.title }}</h1>
      <div class="d-flex justify-content-start mt-4 mb-4">
      <div class="d-inline-block">
        <span class="text-white me-2">평점</span>
        <h5 v-if="vote_average" id="percentage">{{ vote_average }}<span style="font-size: 6px;">%</span></h5>
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
    <div id="review" class="pb-5">
      <!-- 리뷰 작성 -->
      <div class="chat-container" style="background-color: rgba(255, 255, 255, 0.9); height: 65px; padding: 10px;">
        <vs-input icon="mode_edit" class="inputx review-input text-start" v-model="reviewText" :placeholder="nickname+'님, 남기고 싶은 말이 있으신가요?'" @keypress.enter="createReview"/>
      </div>
      <vs-collapse accordion class="p-0">
        <div v-for="(review, idx) in reviews" :key="idx" class="chat-container d-flex align-items-center" style="background-color: rgba(255, 255, 255, 0.9); transition: 0.3s">
          <vs-collapse-item class="w-100">
            <div slot="header" class="d-flex justify-content-start align-items-center">
              <!-- <img :src="SERVER_URL+review.user.image" alt="Avatar" style="width:100%; margin-left: 10px;"> -->
              <img v-if="SERVER_URL+review.user.image === SERVER_URL+'null'" src="@/assets/default_profile.jpg" alt="Avatar" style="width:100%; margin-left: 10px;">
              <img v-else :src="SERVER_URL+review.user.image" alt="Avatar" style="width:100%; margin-left: 10px;">
              <!-- 너무 긴 리뷰가 적힐 경우 ...으로 축약 -->
              <span class="me-3">{{ review.user.nickname }}</span>
              <p class="m-0 text-truncate text-start fw-bold" style="font-size: 17px; opacity: 0.8;">{{ review.content }}</p>
              <span v-if="checkNew(humanize(now, review.created_at))" class="badge rounded-pill bg-primary" style="font-size: 10px;">New</span>
              <span v-if="review.comments_count > 4" class="badge rounded-pill bg-danger" style="margin-left: 10px; font-size: 10px;">Hot</span>
            </div>

            <!-- 본문 -->
            <div class="d-flex justify-content-between align-items-end">
              <p class="text-start" style="word-break: break-all; margin-left: 15rem;">{{ review.content }}
                <br><br>
                <vs-avatar class="comment-button" :badge="review.comments_count" color="dark" icon="mode_comment" style="position: relative; top: 1.5rem; left: -0.2rem;" 
                  @mousedown="$router.push({ name: 'Comment', query: { movie: selectedMovie, review: review.id } })"/>
              </p>
              <span v-if="humanize(now, review.created_at) === humanize(now, review.updated_at)" style="margin-right: 1.5rem;">작성: {{ humanize(now, review.created_at) }}</span>
              <span v-else style="margin-right: 1.5rem;">수정: {{ humanize(now, review.updated_at) }}</span>
              <span></span>
            </div>
          </vs-collapse-item>
        </div>
      </vs-collapse>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'
import { mapState } from 'vuex'

export default {
  name: 'Detail',
  data: function () {
    return {
      originalRate: 0,
      currentRate: 1,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      reviewText: '',
      commentText: '',
      selectedMovie: '',
      selectedMovieInfo: {},
      reviews: [],
      comments: [],
      windowWidth: parseInt(screen.availWidth)+"px",
      isPhototicket: false,
      tooltip: '',
      director: '',
      actors: [],
      pageNum: 1,
      possiblePageNum: 2,
      SERVER_URL: SERVER.URL,
      now: new Date(),
    }
  },
  methods: {
    // 리뷰 조회(인피니트 스크롤)
    getReviews: function () {
      this.now = new Date()
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config,
        params: {
          page_num: this.pageNum,
        },
      })
      .then((res)=>{
        this.possiblePageNum = res.data.pop()['possible_page']
        if (this.pageNum === 1) {
          this.reviews = res.data
        } else {
          this.reviews.push(...res.data)
        }
        this.pageNum += 1
      })
    },
    detailCheckBottom: function () {
      const {scrollTop, clientHeight, scrollHeight} = document.documentElement
      if (scrollHeight - scrollTop <= clientHeight) {
        if (this.pageNum <= this.possiblePageNum) {
          this.getReviews()
        }
      }
    },
    // 리뷰 생성
    createReview: function () {
      const content = this.reviewText
      this.now = new Date()
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config,
        data: {
          content,
        }
      })
      .then(res => {
        this.reviews.unshift(res.data)
        this.reviewText = ''
      })
      .catch(err => {
        console.log(err)
      })
    },
    // 별점 주기
    giveRate: function () {
      const rate = this.currentRate
      this.$vs.notify({title:`${this.nickname}님! ${this.currentRate}점 후원 감사합니다! 😘`, text: '추천 영화에 반영됩니다 💘' ,color:'warning',icon:'star'})
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
          this.originalRate = res.data.rate
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
    humanize: function (now, date) {
      const moment = require('moment')
      const dateData = new Date(date)
      let r = now - dateData
      if (parseInt(r) > 43200000) {
        r = moment(dateData).format('YY.MM.DD\u00A0\u00A0HH:MM')
      } else if (parseInt(r) >= 3600000) {
        r = parseInt(parseInt(r) / 3600000).toString() + '시간 전'
      } else if (parseInt(r) >= 60000) {
        r = parseInt(parseInt(r) / 60000).toString() + '분 전'
      } else {
        r = '방금 전'
      }
      return r
    },
    checkNew: function (time) {
      if (time.includes('전')) {
        return true
      } else {
        return false
      }
    },
  },
  // main page에서 카드를 눌렀을 때 detail page로 이동된 것
  // detail page가 실행되자마자 영화정보, 영화에 대한 리뷰, 유저가 준 rating, 
  created() {
    const moviePk = this.$route.query.moviePk
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
    // 별점정보
    axios ({
      method: 'get',
      url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates`,
      headers: this.$store.getters.config
    })
    .then(res => {
      this.originalRate = res.data.rate
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
    document.addEventListener('scroll', this.detailCheckBottom)
  },
  destroyed: function () {
    document.removeEventListener('scroll', this.detailCheckBottom)
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
  },
  watch: {
    originalRate: function (curVal) {
      this.currentRate = curVal / 20
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

#logo {
  position: absolute;
  top: 1rem;
  left: 1rem;
  color: #f1f1f1;
  opacity: 0.7;
  font-size: 2rem;
  cursor: pointer;
}

#poster {
  position: absolute;
  top: 5rem;
  left: 23.5rem; 
}

#sideText {
  color: whitesmoke;
  font-size: 1.5rem;
  position: fixed;
  top: 20vh;
  left: 2vw;
  opacity: 0;
  animation-name: slideSide;
  animation-duration: 6s;
}

#sidetext > h1 {
  font-family: 'Nanum Myeongjo', serif;
}

@keyframes slideSide {
  0% {
    left: -10vw;
    opacity: 0;
  }
  20% {
    left: 1vw;
    opacity: 1;
  }
  80% {
    left: 1vw;
    opacity: 1;
  }
  100% {
    left: -5vw;
  }
}

#movie-title{
  width: 50rem;
}

#movie-overview{
  width: 50rem;
  height: 5rem;
  white-space: normal;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2; 
  height: 3.6em;
  word-wrap: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

#info-div{
  position: absolute; 
  top: 10rem;
  left: 43.5rem;;
}

#percentage{
  position: absolute; 
  top: 5.6rem;
  left: 3.5rem;
  color: white;
}

#add-photo-ticket-icon {
  color: white;
  background-color: rgb(12, 37, 63);
}

#remove-photo-ticket-icon {
  color: crimson;
  background-color: rgb(12, 37, 63);
}

#review{
  position: absolute;
  top: 35rem;
  left: 23.5rem;
  width: 70rem;
}

#Detail {
  background-color: #1414144b;
}

.chat-container {
  border: 2px solid #dedede;
  background-color: #f1f1f1;
  border-radius: 5px;
  margin: 10px 0;
}

.chat-container p {
  width: 55%;
  display: inline-block;
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
  margin-right: 10px;
  border-radius: 50%;
}

.chat-container img.right {
  float: right;
  margin-left: 20px;
  margin-right:0;
}

.review-input {
  width: 90% !important;
  display: inline !important;
  margin-left: 0rem;
}

.comment-button:hover {
  transform-origin: top;
  animation: bell 2s infinite linear;
}

@keyframes bell{
  0%, 50%{
    transform: rotate(0deg);
	}
  5%, 15%, 25%, 35%, 45% {
    transform: rotate(13deg);
  }
  10%, 20%, 30%, 40% {
    transform: rotate(-13deg);
  }
}
</style>

<style lang="stylus">
.default-input
  .inputx
    margin 10px
</style>