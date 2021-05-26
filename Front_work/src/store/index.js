import Vue from 'vue'
import Vuex from 'vuex'
import SERVER from '@/api/drf.js'
import router from '@/router/index.js'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

import axios from 'axios'
import swal from 'sweetalert'

export default new Vuex.Store({
  // 새로고침을 해도 state 정보가 날아가지 않도록 하는 플러그인 persistedstate
  plugins: [createPersistedState()],
  state: {
    authToken: localStorage.getItem('jwt'),
    videoKey: '',
    nickname: '',
    image: '',
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
      return `https://www.youtube.com/embed/${state.videoKey}?controls=1&rel=0&autoplay=1&mute=1&loop=1&playlist=${state.videoKey}`
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
    GET_PROFILE: function (state, data) {
      state.nickname = data.nickname
      state.image = data.image
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
        this.dispatch('getProfiles')
        router.push({ name: 'Main' })
      })
      .catch((err) => {
        console.log(err)
        swal ("아이디와 비밀번호를 확인해주세요", {
          dangerMode: true,
        })
      })
    },
    logout: function ({ commit }) {
      commit('REMOVE_TOKEN')
      router.push({ name: 'Login' })
    },
    signup: function (context, credentials) {
      axios({
        url: SERVER.URL + SERVER.ROUTES.signup,
        method: 'post',
        data: credentials,
      })
      .then(() => {
        router.push({ name: 'Login' })
        this.dispatch('login', credentials)
      })
      .catch((err) => {
        console.log(err)
        swal ("아이디와 비밀번호를 확인해주세요", {
          dangerMode: true,
        })
      })
    },
    getProfiles: function ({ commit, getters }) {
      console.log('바뀜')
      axios({
        method: 'get',
        url: `${SERVER.URL}/api/v2/profile/`,
        headers: getters.config,
      })
      .then((res) => {
        const nickname = res.data.nickname
        const image = `${SERVER.URL}` + res.data.image
        commit('GET_PROFILE', {nickname, image})
      })
      .catch((err) => {
        console.log(err)
      })
    },
    profileUpdate: function ({ commit, getters }, credentials) {
      axios({
        method: 'put',
        url: `${SERVER.URL}/api/v2/profile/`,
        data: credentials,
        headers: getters.config,
      })
      .then((res) => {
        const nickname = res.data.nickname
        const image = `${SERVER.URL}` + res.data.image
        commit('GET_PROFILE', {nickname, image})
      })
      .catch((err) => {
        console.log(err)
        swal ("일치하는 닉네임이 존재합니다!", {
          dangerMode: true,
        })
      })
    },
    fetchVideos: function ({ commit }, movie_id) {
      axios({
        url: `https://api.themoviedb.org/3/movie/${movie_id}/videos?api_key=${process.env.VUE_APP_TMDB_API_KEY}&region=KR&language=ko`,
        method: 'get', 
      })
      .then((res) => {
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