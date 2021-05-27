<template>
  <div id='Detail'>
    <!-- 배경 -->
    <h1 id='logo' @click="$router.push({ name: 'Main' })">MET<span style="color: rgba(140, 100, 172, 0.8);">MIX</span>A</h1>
    <img id="bg-backdrop" :src="this.selectedMovieInfo.backdrop_path" alt="" :style="{ width: windowWidth }">
    <div id="bg-cover" :style="{ width: windowWidth }"></div>
    <img id="poster" :src="this.selectedMovieInfo.poster_path" rounded alt="" style="width: 300px; border-radius: 7px;">
    
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
    
    <!-- Review 정보 보여주기 -->
    <div id="comment" class="pb-5">
      <div style="width: 100%; background-color: rgb(231, 231, 230); border-radius: 5px;">
        <div class="review-container" style="width: 100%; background-color: rgb(231, 231, 230); border-radius: 5px;">
          <div class="d-flex align-items-center">
            <img v-if="SERVER_URL+selectedReviewInfo.user.image === SERVER_URL+'null'" src="@/assets/default_profile.jpg" alt="Avatar">
            <img v-else :src="SERVER_URL+selectedReviewInfo.user.image" alt="Avatar">
            <p class="text-start" style="padding-top: 2.7rem; padding-left: 6rem; padding-bottom: 1.4rem; margin-bottom: 0.2rem; opacity: 0.8;">
              <span class="fw-bold me-2">{{ selectedReviewInfo.user.nickname }}</span> | 
              <span v-if="humanize(now, review.created_at) === humanize(now, review.updated_at)" class="ms-2">{{ humanize(now, selectedReviewInfo.created_at) }}</span>
              <span v-else class="ms-2">{{ humanize(now, selectedReviewInfo.updated_at) }}</span>
            </p>
            <vs-dropdown :vs-trigger-click="true" v-if="nickname === selectedReviewInfo.user.nickname" style="margin-left: 48.75rem; top: -0.7rem;">
              <a class="a-icon text-dark" style="opacity: 1;" href="#">
                <span class="material-icons">more_vert</span>
              </a>
              <vs-dropdown-menu>
                <vs-dropdown-item>
                  <div style="d-flex align-items-baseline">
                    <span class="material-icons me-1" style="position: relative; top: 5px;" @click="isReviewUpdating=true">edit</span>
                    <button @mousedown="currentReviewText=selectedReviewInfo.content" @click="isReviewUpdating=true">수정</button>
                  </div>
                </vs-dropdown-item>
                <vs-dropdown-item>
                  <span class="material-icons me-1" style="position: relative; top: 5px;" @click="deleteReview(selectedReview)">delete</span>
                  <button @click="openReviewConfirm(selectedReview)">삭제</button>
                </vs-dropdown-item>
              </vs-dropdown-menu>
            </vs-dropdown>
          </div>
          <hr>
          <!-- review 수정 input -->
          <div v-if="isReviewUpdating" style="width:90%; margin-left: 3.5rem; padding: 2rem 0 2rem 0;">
            <vs-input size="large" label-placeholder="리뷰 수정" class="inputx review-input text-start" style="margin: 2rem 10px 10px 10px; width: 1100px; word-break: break-all;"
              v-model="currentReviewText"  @keypress.enter="updateReview(selectedReview)" @blur="isReviewUpdating = ''"/> 
          </div>
          <p v-if="!isReviewUpdating" class="text-start" style="margin: 3rem 10rem 0 10rem; padding-bottom: 3rem; word-break: break-all;">{{ currentReviewText }}</p>
        </div>
        <!-- comments -->
        <!-- 댓글 생성 -->
      </div>
      <div style="background-color: rgba(255, 255, 255, 0.9); height: 65px; margin-top: 30px; padding: 10px; border-radius: 5px;">
        <vs-input icon="mode_edit" class="comment-input input text-start ms-1" placeholder="댓글을 입력해보세요" v-model="commentText" @keypress.enter="createComment"/>
      </div>
      <div>
        <div v-for="(comment, idx) in comments" :key="idx" class="comment-container" style="background-color: rgba(255, 255, 255, 0.9); transition: 0.3s">
          <div class="d-flex align-items-center">
            <span class="material-icons" style="transform:rotate(180deg); margin-top: 0.5rem; margin-left: 0.5rem;">reply</span>
            <img v-if="SERVER_URL+comment.user.image === SERVER_URL+'null'" src="@/assets/default_profile.jpg" alt="Avatar">
            <img v-else :src="SERVER_URL+comment.user.image" alt="Avatar">
            <p class="text-start"><span class="fw-bold me-2">{{ comment.user.nickname }}</span>|<span v-if="humanize(now, comment.created_at) === humanize(now, comment.updated_at)" class="ms-2">{{ humanize(now, comment.created_at) }}</span>
              <span v-else class="ms-2">{{ humanize(now, selectedReviewInfo.updated_at) }}</span>
            </p>
            <vs-dropdown :vs-trigger-click="true" v-if="nickname === comment.user.nickname" style="margin-left: 50rem;">
              <a class="a-icon text-dark" style="opacity: 0.8;" href="#">
                <span class="material-icons">more_vert</span>
              </a>
              <vs-dropdown-menu>
                <vs-dropdown-item>
                  <div style="d-flex align-items-baseline">
                    <span class="material-icons me-1" style="position: relative; top: 5px;" @click="getComment(comment.content, idx)">edit</span>
                    <button @click="getComment(comment.content, idx)">수정</button>
                  </div>
                </vs-dropdown-item>
                <vs-dropdown-item>
                  <span class="material-icons me-1" style="position: relative; top: 5px;" @click="deleteComment(comment.id)">delete</span>
                  <button @click="openCommentConfirm(comment.id)">삭제</button>
                </vs-dropdown-item>
              </vs-dropdown-menu>
            </vs-dropdown>
          </div>
          <div>
            <p class="text-start" style="word-break: break-all; padding-left: 5.16rem; padding-top: 0rem; padding-right: 5.16rem;">{{ comment.content }}</p>
          </div>
          <div>
            <!-- 댓글 수정 -->
            <!-- 현재 수정 버튼의 인덱스의 글에서 수정창 등장 -->
            <vs-input v-if="idx===currentCommentIdx" icon="mode_edit"
              ref="commentUpdateInput" class="inputx text-start" style="margin-start: 8px; margin-bottom: 8px; width: 1100px; margin-end: 10px;"
              v-model="currentCommentText" @keypress.enter="updateComment($event, comment.id)" @blur="currentCommentIdx = ''"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'
import { mapState } from 'vuex'
import swal from 'sweetalert'

export default {
  name: 'Comment',
  data: function () {
    return {
      originalRate: 0,
      currentRate: 1,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      selectedMovie: '',
      selectedMovieInfo: {},
      selectedReview: '',
      selectedReviewInfo: {},
      currentReviewText: '',
      commentText: '',
      comments: [],
      currentCommentText: '',
      currentCommentIdx: '',
      windowWidth: parseInt(screen.availWidth)+"px",
      isPhototicket: false,
      tooltip: '',
      director: '',
      actors: [],
      pageNum: 1,
      possiblePageNum: 2,
      SERVER_URL: SERVER.URL,
      review: {},
      isReviewUpdating: false,
      activeConfirm:false,
      deleteReviewPk: -1,
      deleteCommentPk: -1,
      now: new Date(),
    }
  },
  methods: {
    // 별점 주기
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
    // 리뷰 삭제 컨펌
    openReviewConfirm(reviewPk) {
      this.deleteReviewPk = reviewPk
      this.$vs.dialog({
        type:'confirm',
        color: 'rgba(140, 100, 172)',
        title: `삭제`,
        text: '리뷰를 삭제하시겠습니까?',
        accept:this.deleteReview
      })
    },
    // 댓글 삭제 컨펌
    openCommentConfirm(commentPk) {
      this.deleteCommentPk = commentPk
      this.$vs.dialog({
        type:'confirm',
        color: 'rgba(140, 100, 172)',
        title: `삭제`,
        text: '댓글을 삭제하시겠습니까?',
        accept:this.deleteComment
      })
    },
    // 리뷰 수정
    updateReview: function (reviewPk) {
      const newReview = this.currentReviewText
      this.now = new Date()
      axios({
        method: 'put',
        url: `${SERVER.URL}/api/v1/reviews/${reviewPk}/`,
        headers: this.$store.getters.config,
        data: {
          'content': newReview
        }
      })
      // 리뷰 갱신
      .then(() => {
        this.isReviewUpdating = false
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 리뷰 삭제 
    deleteReview: function () {
      axios({
        method: 'delete',
        url: `${SERVER.URL}/api/v1/reviews/${this.deleteReviewPk}`,
        headers: this.$store.getters.config,
      })
      // db에서 삭제 후 Detail page로 이동(현재를 history에 남기지 않게 됨)
      .then(() => {
        this.$router.go(-1)
      })
      .catch(err => {
        console.log(err)
        swal ("자신의 댓글만 지워주세요!", {
          dangerMode: true,
        })
      })
    },
    // 댓글 조회
    getComments: function () {
      this.now = new Date()
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/reviews/${this.$route.query.review}/comments/`,
        headers: this.$store.getters.config,
      })
      .then((res)=>{
        this.comments = res.data
      })
    },
    // 댓글 생성
    createComment: function () {
      const content = this.commentText
      this.now = new Date()
      axios({
        method: 'post',
        url: `${SERVER.URL}/api/v1/reviews/${this.selectedReviewInfo.id}/comments/`,
        headers: this.$store.getters.config,
        data: {
          content,
        }
      })
      .then(res => {
        this.comments.unshift(res.data)
        this.commentText = ''
      })
      .catch(err => {
        console.log(err)
      })
    },
    // 단일 댓글 조회 (댓글 수정 사전 작업)
    // idx : 수정 버튼의 인덱스
    getComment: function (commentContent, idx) {
      this.currentCommentText = commentContent
      this.currentCommentIdx = idx
    },
    // 댓글 수정
    updateComment: function ($event, commentPk) {
      const newComment = $event.target.value
      this.now = new Date()
      axios({
        method: 'put',
        url: `${SERVER.URL}/api/v1/comments/${commentPk}/`,
        headers: this.$store.getters.config,
        data: {
          'content': newComment
        }
      })
      // 댓글 갱신
      .then(() => {
        this.getComments()
        this.currentCommentIdx = ''
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 댓글 제거
    deleteComment: function () {
      this.now = new Date()
      axios({
        method: 'delete',
        url: `${SERVER.URL}/api/v1/comments/${this.deleteCommentPk}`,
        headers: this.$store.getters.config,
      })
      .then(() => {
        this.getComments()
      })
      .catch(err => {
        console.log(err)
        swal ("자신의 댓글만 지워주세요!", {
          dangerMode: true,
        })
      })
  }},
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
      this.currentReviewText = res.data.content
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
    this.getComments()
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

#comment{
  position: absolute;
  top: 35rem;
  left: 23.5rem;
  width: 70rem;
}

.review-container img {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 60px;
  margin-right: 20px;
  border-radius: 50%;
}

.comment-input {
  width: 90% !important;
  display: inline !important;
  top: -1.3rem;
}

.comment-container {
  border: 2px solid #dedede;
  background-color: #f1f1f1;
  border-radius: 5px;
  margin: 10px 0;
}

.comment-container img {
  top: 1.5rem;
  left: 1.5rem;
  width: 45px;
  border-radius: 50%;
  margin-left: 0.3rem;
  margin-top: 0.5rem;
}

.comment-container p {
  opacity: 0.8;
  padding-top: 1.5rem;
  margin-left: 0.7rem;
  font-size: 15px;
}
</style>