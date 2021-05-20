import Vue from 'vue'
import App from './App.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import VueFullPage from 'vue-fullpage.js'
import router from './router'
import store from './store'

Vue.config.productionTip = false
Vue.use(VueFullPage)

new Vue({
  created() {
    AOS.init();
  },

  router,
  store,
  render: h => h(App)
}).$mount('#app')
