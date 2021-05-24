import Vue from 'vue'
import App from './App.vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import VueFullPage from 'vue-fullpage.js'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BCard } from 'bootstrap-vue'
import ElementUI from "element-ui";
import Carousel3d from 'vue-carousel-3d';


Vue.config.productionTip = false
Vue.use(VueFullPage)
Vue.use(BootstrapVue)
Vue.component('b-card', BCard)
Vue.use(ElementUI);
Vue.config.productionTip = false;
Vue.use(Carousel3d)

new Vue({
  created() {
    AOS.init();
  },

  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
