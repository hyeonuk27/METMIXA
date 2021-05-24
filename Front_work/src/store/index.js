import Vue from 'vue'
import Vuex from 'vuex'
import SERVER from '@/api/drf.js'
import router from '@/router/index.js'

Vue.use(Vuex)

import axios from 'axios'

export default new Vuex.Store({
  state: {
    authToken: localStorage.getItem('jwt'),
    videoKey: '',
  },
  getters: {
    isLoggedIn: function (state) {
      return state.authToken ? true : false
    },
    config: function (state) {
      return {
        Authorization: `JWT ${state.authToken}`
      }
    },
    videoURI: function (state) {
      return `https://www.youtube.com/embed/${state.videoKey}?autoplay=1&mute=1&loop=1&playlist=${state.videoKey}`
    },
  },
  mutations: {
    SET_TOKEN: function (state, token) {
      state.authToken = token
      localStorage.setItem('jwt', token)
    },
    REMOVE_TOKEN: function (state) {
      localStorage.removeItem('jwt')
      state.authToken = ''
    },
    SET_VIDEO_KEY: function (state, key) {
      state.videoKey = key
    }
  },
  actions: {
    login: function ({ commit }, credentials) {
      axios({
        url: SERVER.URL + SERVER.ROUTES.login,
        method: 'post',
        data: credentials,
      })
      .then((res) => {
        commit('SET_TOKEN', res.data.token)
        router.push({ name: 'Main' })
        // 추가로 고쳐야 함
      })
      .catch((err) => {
        console.log(err)
      })
    },
    logout: function ({ commit }) {
      commit('REMOVE_TOKEN')
      router.push({ name: 'Login' })
    },
    signup: function (context, credentials) {
      // const config = {
      //   'Content-Type': 'multipart/form-data',
      // }
      console.log(credentials)
      axios({
        url: SERVER.URL + SERVER.ROUTES.signup,
        method: 'post',
        data: credentials,
        // headers: config,
      })
      .then(() => {
        router.push({ name: 'Login' })
        this.dispatch('login', credentials)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    fetchVideos: function ({ commit }, movie_id) {
      axios({
        url: `https://api.themoviedb.org/3/movie/${movie_id}/videos?api_key=${process.env.VUE_APP_TMDB_API_KEY}&region=KR&language=ko`,
        method: 'get', 
      })
      .then((res) => {
        console.log(res.data.results[0].key)
        commit('SET_VIDEO_KEY', res.data.results[0].key)
      })
      .catch((err) => {
        console.log(err)
      })
    }
  },
  modules: {
  }
})