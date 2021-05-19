import Vue from 'vue'
import App from './App.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import VueFullPage from 'vue-fullpage.js'
import router from './router'

Vue.config.productionTip = false
Vue.use(VueFullPage)

new Vue({
  created() {
    AOS.init();
  },

  router,
  render: h => h(App)
}).$mount('#app')
