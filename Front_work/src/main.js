import Vue from 'vue'
import App from './App.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import VueFullPage from 'vue-fullpage.js'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false
Vue.use(VueFullPage)

new Vue({
  created() {
    AOS.init();
  },

  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
