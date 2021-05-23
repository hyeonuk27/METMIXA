<template>
<div id="example">
  <carousel-3d width='180' class="img" ref="treeExplorer" :space="250" @after-slide-change="goDetail">
    <slide v-for="(movie, i) in movieList" :key="i" :index="i" style="border: black solid 1px;">
      <div @click="fetchVideos(movie.tmdb_id)" style="cursor: pointer; height: 100%;">
        <img :src="movie.poster_path" style="height: 100%;">
      </div>
    </slide>
  </carousel-3d>
</div>
</template>

<script>
import { Carousel3d, Slide } from 'vue-carousel-3d';
import { mapActions } from 'vuex'

export default {
  name: 'MovieList',
  props: {
    movieList: {
      type: Array,
    }
  },
  components: {
    Carousel3d,
    Slide,
  },
  data: function () {
    return {
      items: [],
      trigger: 0,
    }
  },
  methods: {
    ...mapActions([
      'fetchVideos',
    ]),
    goDetail: function (event) {
      const moviePk = this.movieList[event].id
      this.$router.push({ 
        name: 'Detail',
        query: { moviePk }
      })
    }
  },
  created: function () {
  }
}
</script>

<style>
.img {
  position: fixed;
  top: 32rem;
  height: 100%;
  width: 100%;
  transform: rotateX(10deg);
  /* transform: rotateY(0) */
  opacity: 0.7;
  transition: 0.3s;
}

.img:hover {
  opacity: 1;
}
</style>