<template>
  <div id='Main'>
    <h1 id='logo' @click="uncheck">METMIXA</h1>
    <iframe width="854" height="480" :src="videoURI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <!-- <img id="bg" :src="movieList[0].backdrop_path" alt=""> -->
    <input type="checkbox" id="my-menu"><label for="my-menu"><img src="@/assets/default_profile.jpg"></label>
    <div class="sidebar">
      <div id="menu1" class="menu mb-2 text-start fw-bold" @click="$router.push({ name: 'Profile' })">
        <span>포토티켓</span>
      </div>
      <div class="menu text-start fw-bold" @click="logout">
        <span>로그아웃</span>
      </div>
    </div>
    <MovieList :movieList="movieList" @click.native="uncheck"/>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from 'axios'
import MovieList from '@/components/MainPage/MovieList'

export default {
  name: 'Main',
  components: {
    MovieList,
  },
  data() {
    return {
      movieList: [],
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
  },
  computed: {
    ...mapGetters([
      'config',
      'videoURI'
    ])
  },
  created: function () {
    axios({
        method: 'get',
        // 장고한테 요청
        url: 'http://127.0.0.1:8000/api/v1/movies/',
        params: {
          mode: 'algorithm',
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
  }
}
</script>

<style scoped>

/* img {
  position: fixed; 
  top: 0; 
  left: 0; 
  min-width: 100%;
  min-height: 100%;
} */

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
  width: 200px;
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
  margin-top: 6rem;
}

.menu {
  margin-left: 1rem;
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

</style>