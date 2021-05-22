import Vue from 'vue'
import Vuex from 'vuex'
import SERVER from '@/api/drf.js'
import router from '@/router/index.js'
import axios from 'axios'
Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authToken: localStorage.getItem('jwt'),
  },
  getters: {
    isLoggedIn: function (state) {
      return state.authToken ? true : false
    },
    config: function (state) {
      return {
        Authorization: `JWT ${state.authToken}`
      }
    }
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
  },
  modules: {
  }
})