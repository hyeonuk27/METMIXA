<template>
  <div id='Main'>
    <h1 id='logo'>METMIXA</h1>
    <vs-select
      class="selectMode"
      v-model="mode"
      color="#123763"
      @change="selectMode"
      >
      <vs-select-item :key="index" :value="item.value" :text="item.text" v-for="item,index in modes"/>
    </vs-select>
    <vs-input class="selectInput" color="rgba(255, 255, 255, 0.5)" v-model="selectInputValue"/>
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; opacity: 0;" @click="uncheck"></div>
    <iframe width="1920" height="1080" :src="videoURI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <input type="checkbox" id="my-menu">
    <label for="my-menu">
      <img v-if="image === SERVER_URL+'null'" src="@/assets/default_profile.jpg">
      <img v-else :src="image">
    </label>
    <div class="sidebar">
      <div id="menu1" class="menu mb-3 text-end fw-bold" @click="$router.push({ name: 'Profile' })">
        <span>내 프로필</span>
      </div>
      <div class="menu text-end fw-bold mb-3" @click="logout">
        <span>로그아웃</span>
      </div>
      <div v-if="nickname === '어드민'" class="menu text-end fw-bold">
        <a href="http://127.0.0.1:8000/admin" class="text-decoration-none">관리자 페이지</a>
      </div>
    </div>
    <MovieList :movieList="movieList" @mousedown.native="uncheck"/>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import axios from 'axios'
import MovieList from '@/components/Main/MovieList'
import SERVER from '@/api/drf.js'

export default {
  name: 'Main',
  components: {
    MovieList,
  },
  data() {
    return {
      movieList: [],
      SERVER_URL: SERVER.URL,
      mode: 'algorithm',
      modes:[
        {text:'추천 영화',value: 'algorithm'},
        {text:'인기순',value: 'popularity'},
        {text:'최신순',value: 'release_date'},
        {text:'평점순',value: 'vote_average'},
        {text:'영화명',value: 'title'},
        {text:'감독명',value: 'director'},
        {text:'배우명',value: 'actor'},
        {text:'장르별',value: 'genre'},
      ],
      selectInputValue: '',
    }
  },
  methods: {
    ...mapActions([
      'logout',
      'fetchVideos',
    ]),
    uncheck: function () {
      const myMenu = document.querySelector('#my-menu')
      myMenu.checked = false
    },
    getMoviesByMode: function (mode) {
      axios({
        method: 'get',
        // 장고한테 요청
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode,
        },
        headers: this.config
      })
      .then((res)=>{
        // 응답 데이터에서 가능한 페이지 수 데이터만 pop해서 가져온다.
        this.movieList = res.data
        this.fetchVideos(this.movieList[0].tmdb_id)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    selectMode: function (mode) {
      if (['algorithm', 'release_date', 'popularity', 'vote_average'].includes(mode)) {
        this.getMoviesByMode(mode)
      }
    }
  },
  computed: {
    ...mapState([
      'image',
      'nickname',
    ]),
    ...mapGetters([
      'config',
      'videoURI'
    ])
  },
  created: function () {
    this.getMoviesByMode('algorithm')
  }
}
</script>

<style scoped>
#my-menu + label{
  position: fixed;
  z-index: 3;
  top: 1.6rem;
  right: 2.2rem;
  width: 45px;
  height: 45px;
  border-radius: 100%;
  cursor: pointer;
  transition: .3s;
}
#my-menu + label > img {
  border-radius: 100%;
}
#my-menu + label:hover {
  transform: translateY(1.5px) rotate(-10deg);
  opacity: .7;
}
input[type=checkbox] { 
  display:none
}
div[class=sidebar] {
  width: 170px;
  height: 100%;
  background: #222;
  opacity: 0.95;
  position: fixed;
  top: 0;
  right: -200px;
  z-index: 2;
  transition: all .35s;
}
input[type=checkbox]:checked + label + div {
  right: 0;
}
#menu1 {
  margin-top: 6.5rem;
}
.menu {
  margin-right: 2.1rem;
  color: #818181;
  cursor: pointer;
  font-size: 1.2rem;
}
.menu > span:hover {
  color: #f1f1f1;
}
#Main > iframe {
  z-index: -1;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
#logo {
  position: fixed;
  top: 1rem;
  left: 0.75rem;
  color: #f1f1f1;
  opacity: 0.7;
  font-size: 3.2rem;
}
.con-select {
  z-index: 5;
  top: 5rem;
  left: 0.75rem;
  color: white;
  opacity: 0.8;
}
.selectInput {
  z-index: 5;
  top: 5rem;
  width: 212px;
  color: rgba(255, 255, 255, 0.8);
  padding-left: 12px;
}
</style>

<style lang="scss">
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  background: #ffffff;
}
::-webkit-scrollbar-thumb {
  border-radius: 3.5px;
  background-color: #123763;

  &:hover {
    background-color: #364d69;
  }
}
::-webkit-scrollbar-track {
  background: #ffffff;
}
</style>