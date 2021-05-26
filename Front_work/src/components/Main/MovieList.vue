<template>
<div id="example">
  <div class="img d-flex justify-content-center">
    <carousel-3d
      width='180'
      ref="treeExplorer"
      :space="270"
      :count="movieList.length"
      :display="7"
      @after-slide-change="setSelectedMovieId"
      @before-slide-change="play"
      >
      <slide v-for="(movie, i) in movieList" :key="i" :index="i">
        <div @click="fetchVideos(movie.tmdb_id)" style="cursor: pointer; height: 100%;">
          <img :src="movie.poster_path" style="height: 100%;">
        </div>
      </slide>
    </carousel-3d>
    <div id="card-cover">
      <h6 style="color: white; padding: 10px; margin-top: 40px;">{{title}}</h6>
      <h6 style="color: white;">평점 {{ vote_average }}</h6>
      <!-- {{ movieList[selectedMovieId].tmdb_id }} -->
      <button id="detail-button" @click="goDetail">상세정보<i class="fas fa-chevron-right ms-2" style="font-size: 15px;"></i></button>
    </div>
  </div>
</div>
</template>

<script>
import { Carousel3d, Slide } from 'vue-carousel-3d';
import { mapActions } from 'vuex'

export default {
  name: 'MovieList',
  data: function () {
    return {
      selectedMovieId: '',
      vote_average: 0,
      title: '',
      afterSlide: 0,
    }
  },
  props: {
    movieList: {
      type: Array,
    }
  },
  components: {
    Carousel3d,
    Slide,
  },
  methods: {
    ...mapActions([
      'fetchVideos',
    ]),
    play(event) {
      var audio = new Audio(require('/src/assets/moviesound.mp3'));
      if (((Math.abs(this.afterSlide - event) > 0 && Math.abs(this.afterSlide - event) < 4)) || (this.movieList.length - (Math.abs(this.afterSlide - event)) < 2)) {
        audio.play()
        .catch(err => {
          console.log(err)
        })
      }
    },
    setSelectedMovieId: function (event) {
      this.afterSlide = event
      const movie = this.movieList[event]
      this.selectedMovieId = movie.id
      let average = ((movie.tmdb_vote_sum + movie.our_vote_sum*2) / (movie.tmdb_vote_cnt + movie.our_vote_cnt)).toFixed(1)
      if (average === "NaN") {
        average = '정보 없음'
      }
      this.vote_average = average
      this.title = movie.title
    },
    goDetail: function () {
      const moviePk = this.selectedMovieId
      this.$router.push({ 
        name: 'Detail',
        query: { moviePk }
      })
    }
  },
  created: function () {
  },
  updated: function () {
    this.$refs.treeExplorer.goSlide(this.$refs.treeExplorer.currentIndex)
  },
}
</script>

<style>
.img {
  margin-top: 34rem;
  left: 0%;
  height: 100%;
  width: 100%;
  transform: rotateX(10deg);
  /* transform: rotateY(0) */
  opacity: 0.5;
  transition: 0.3s;
}

.img:hover {
  opacity: 1;
}

#card-cover:not(button, h2, h6) {
  position: absolute;
  /* left: 35%; */
  margin-top: 1.3rem;
  width: 182px;
  height: 270px;
  background-color: black;
  opacity: 0;
  transition: 0.3s;
}

#card-cover:hover {
  opacity: 0.8;
}

#detail-button {
  position: absolute;
  color: white;
  border: white solid 1px;
  padding: 10px;
  left: 2.5rem;
  top: 12rem;
}
</style>