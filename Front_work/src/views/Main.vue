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
    <vs-input v-if="inputMode" autofocus class="select-input" color="rgba(255, 255, 255, 0.5)" v-model="selectInputValue" 
      @focus="inputFocus = true" @blur="inputFocus=false" @keypress.enter="searchInputSubmit($event)"/>
    <span v-if="!inputFocus && inputMode && !selectInputValue" class="mode-icon material-icons">search</span>
    <span v-if="selectedMode === 'algorithm'" class="mode-icon material-icons">recommend</span>
    <span v-if="selectedMode === 'release_date'" class="mode-icon material-icons">schedule</span>
    <span v-if="selectedMode === 'popularity'" class="mode-icon material-icons">auto_awesome</span>
    <span v-if="selectedMode === 'vote_average'" class="mode-icon material-icons">poll</span>
    <span v-if="selectedMode === 'popularity'" class="mode-icon material-icons">auto_awesome</span>
    <div v-if="genreMode" class="genre-cover"></div>
    <span v-if="genreMode" class="material-icons" style="position: absolute; z-index: 8; top: 4.5rem; left: 26.5rem;color: rgba(255, 255, 255, 0.8); cursor: pointer;" 
      @click="genreMode = false">close</span>
    <div v-if="genreMode" class="genre-images">
      <div class="row row-cols-1 row-cols-md-2 g-4" style="width: 70%;">
        <div class="genre-image col" v-for="(image, index) in genreImages" :key="index">
          <div class="card">
            <img :src="SERVER_URL+image" class="card-img-top" alt="genre-img" @click="genreSubmit(index)">
          </div>
        </div>
      </div>
    </div>
    <span v-if="selectedMode === 'genre'" class="dif-genre" @click="genreMode = true">
      <span class="material-icons" style="position: relative; top: 5px; margin-right: 4px;">theaters</span>다른 장르
    </span>
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; opacity: 0;" @click="uncheck"></div>
    <iframe width="1920" height="1080" :src="videoURI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <input type="checkbox" id="my-menu">
    <label for="my-menu">
      <img v-if="image === SERVER_URL+'null'" src="@/assets/default_profile.jpg">
      <img v-else :src="image">
    </label>
    <div class="sidebar">
      <div id="menu1" class="menu mb-3 text-end" @click="$router.push({ name: 'Profile' })">
        <span>내 프로필</span>
      </div>
      <div class="menu text-end mb-3" @click="logout">
        <span>로그아웃</span>
      </div>
      <div v-if="nickname === '어드민'" class="menu text-end">
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
        {text:'장르별',value: 'genre'},
        {text:'인기순',value: 'popularity'},
        {text:'최신순',value: 'release_date'},
        {text:'평점순',value: 'vote_average'},
        {text:'영화명',value: 'title'},
        {text:'감독명(영문)',value: 'director'},
        {text:'배우명(영문)',value: 'actor'},
      ],
      selectInputValue: '',
      selectedMode: 'algorithm',
      inputMode: false,
      inputFocus: false,
      genreImages:[
        '/media/genres/가족.jpg',
        '/media/genres/공포.jpg',
        '/media/genres/다큐.jpg',
        '/media/genres/드라마.jpg',
        '/media/genres/로맨스.jpg',
        '/media/genres/모험.jpg',
        '/media/genres/미스터리.png',
        '/media/genres/범죄.jpg',
        '/media/genres/서부.png',
        '/media/genres/스릴러.jpg',
        '/media/genres/애니메이션.png',
        '/media/genres/액션.png',
        '/media/genres/역사.jpg',
        '/media/genres/음악.png',
        '/media/genres/전쟁.jpg',
        '/media/genres/코미디.png',
        '/media/genres/판타지.png',
        '/media/genres/SF.jpg',
        '/media/genres/TV.png',
      ],
      genreId: {
        0: '10751', 1: '27', 2: '99', 3: '18', 4: '10749', 5: '12', 6: '9648',
        7: '80', 8: '37', 9: '53', 10: '16', 11: '28', 12: '36', 13: '10402',
        14: '10752', 15: '35', 16: '14', 17: '878', 18: '10770',
      },
      genreMode: false,
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
    // 영화 모드 선택
    selectMode: function (mode) {
      this.selectedMode = mode
      this.inputMode = false
      this.selectInputValue = ''
      if (['algorithm', 'release_date', 'popularity', 'vote_average'].includes(mode)) {
        axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode,
        },
        headers: this.config
      })
      .then((res)=>{
        this.movieList = res.data
        this.fetchVideos(this.movieList[0].tmdb_id)
      })
      .catch((err) => {
        console.log(err)
      })
      } else if (['director', 'actor', 'title'].includes(mode)) {
        this.inputMode = true
      } else if (mode === 'genre') {
        this.genreMode = true
      }
    },
    // 인기순, 최신순, 평점순 조회
    getMoviesByMode: function (mode) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode,
        },
        headers: this.config
      })
      .then((res)=>{
        this.movieList = res.data
        this.fetchVideos(this.movieList[0].tmdb_id)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 영화명, 감독명, 배우명 조회
    searchInputSubmit: function ($event) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode: this.selectedMode,
          inputValue: $event.target.value,
        },
        headers: this.config
      })
      .then((res)=>{
        this.movieList = res.data
        this.fetchVideos(this.movieList[0].tmdb_id)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    // 장르별 조회
    genreSubmit: function (index) {
      console.log(this.genreId[index])
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode: this.selectedMode,
          inputGenre: this.genreId[index]
        },
        headers: this.config
      })
      .then((res)=>{
        this.movieList = res.data
        this.genreMode = false
        this.fetchVideos(this.movieList[0].tmdb_id)
      })
      .catch((err) => {
        console.log(err)
        this.$vs.notify({title:'이런!',text:'영화가 아직 없어요😢  업로드를 기대해주세요.',color: 'rgba(0, 0, 0, 0.8)',position:'top-center'})
      })
    },
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
  left: 1rem;
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

.select-input {
  position: fixed;
  z-index: 5;
  top: 7.5rem;
  width: 212px;
  color: rgba(255, 255, 255, 0.8);
  padding-left: 12px;
}

.vs-input--::placeholder {
  color: red;
  font-style: italic;
}

.mode-icon {
  position: fixed;
  color:rgba(255, 255, 255, 0.8);
  top: 7.8rem;
  left: 1.2rem;
  font-size: 2rem;
}

.genre-images {
  z-index: 7;
  position: fixed;
  padding-top: 6rem;
  padding-left: 31rem;
  width: 100%;
  height: 100%;
}

.genre-cover {
  z-index: 6;
  position: fixed;
  top: -0.1rem;
  padding-top: 4rem;
  padding-left: 31rem;
  width: 100%;
  height: 100%;
  background-color: black;
  opacity: 0.8;
}

.genre-image {
  width: 18%;
  padding: 0.1rem;
  margin: 0.1rem;
}

.card {
  background-color: rgba(0, 0, 0, 0);
  border: none;
}

.card > img {
  border-radius: 10px;
  transition: 0.3s;
  cursor: pointer;
}

.card > img:hover {
  width: 95%;
  transform: translateY(1.5px) rotate(-10deg);
}

.dif-genre {
  z-index: 5;
  position: fixed;
  color:rgba(255, 255, 255, 0.8);
  top: 8rem;
  left: 1.2rem;
  cursor: pointer;
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