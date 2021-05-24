<template>
  <div id='Detail'>
    <!-- 배경 -->
    <img id="bg-backdrop" :src="this.selectedMovieInfo.backdrop_path" alt="" :style="{ width: windowWidth }">
    <div id="bg-cover" :style="{ width: windowWidth }"></div>
    <img id="poster" :src="this.selectedMovieInfo.poster_path" rounded alt="" style="width: 300px;">
    
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
          @change="giveRate">
        </el-rate>
        <el-tooltip :content="tooltip" placement="right">
          <v-btn v-if="!isPhototicket" icon id="add-photo-ticket-icon" @click="addMyPhototicket" class="ms-2">
            <v-icon>mdi-heart</v-icon>
          </v-btn>
          <v-btn v-else icon id="remove-photo-ticket-icon" @click="removeMyPhototicket" class="ms-2">
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
    
    <div id="review">
      <!-- 리뷰 작성 -->
      <div class="chat-container" style="background-color: rgba(255, 255, 255, 0.9);">
        <i class="el-icon-edit fs-5" style="margin-top: 3px; margin-left: 0.5rem; margin-right: 2rem;"></i>
        <input class="review-container" v-model="commentText" @keypress.enter="writeComment" placeholder="한 줄 평 작성" style="background-color: rgba(255, 255, 255, 0);">
      </div>
      <div v-for="(review, idx) in reviews" :key="idx" class="chat-container d-flex align-items-center" style="background-color: rgba(255, 255, 255, 0.9);">
        <img src="https://picsum.photos/1000/1000" alt="Avatar" style="width:100%; margin-left: 10px;">
        <!-- 너무 긴 코멘트가 적힐 경우 짤리지 않도록 처리해줘야한다 -->
        <p class="m-0 text-truncate text-start">{{ review.content }}</p>
        <span>{{ review.created_at }}</span>
        <span>{{ review.updated_at }}</span>
        <el-button type="danger" icon="el-icon-delete" circle @click="deleteComment(review.id, idx)" style="margin-left: 110px;"></el-button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'Detail',
  data: function () {
    return {
      //  별점 주기
      originalRate: '',
      currentRate: 1,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      commentText: '',
      selectedMovie: '',
      selectedMovieInfo: {},
      reviews: [],
      windowWidth: parseInt(screen.availWidth)+"px",
      isPhototicket: false,
      tooltip: '',
      director: '',
      actors: [],
      pageNum: 1,
      possiblePageNum: 2,
    }
  },
  methods: {
    // 리뷰 조회(인피니트 스크롤)
    getReviews: function () {
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
        this.reviews.push(...res.data)
        this.pageNum += 1
      })
    },
    checkBottom: function () {
      const {scrollTop, clientHeight, scrollHeight} = document.documentElement
      if (scrollHeight - scrollTop <= clientHeight) {
        if (this.pageNum <= this.possiblePageNum) {
          this.getReviews()
        }
      }
    },
    writeComment() {
      const content = this.commentText
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/reviews/`,
        headers: this.$store.getters.config,
        data: {
          content
        }
      })
      // 리뷰 생성 성공
      .then(res => {
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
        url: `${SERVER.URL}/api/v1/reviews/${reviewPk}`,
        headers: this.$store.getters.config,
      })
      // db에서 삭제 후 vue에서 삭제
      .then(() => {
        this.reviews.splice(idx, 1)
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
          url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates/`,
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
          url: `${SERVER.URL}/api/v1/movies/${this.selectedMovie}/rates/`,
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
    }
  },
  // main page에서 카드를 눌렀을 때 detail page로 이동된 것
  // detail page가 실행되자마자 영화정보, 영화에 대한 리뷰, 유저가 준 rating, 
  // django와 통신은 잘됨
  created() {
    // console.log(this.$store.state.authToken)
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
      console.log(res.data.name)
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
  top: 5rem;
  left: 23.5rem; 
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
.review-container {
  width: 90% !important;
  display: inline !important;
  margin-left: 0rem;
}
</style>