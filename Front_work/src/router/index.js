import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import FullPageScroll from '@/views/FullPageScroll.vue'
import AOS from '@/views/AOS.vue'
import MainScroll from '@/views/MainScroll.vue'
import AnimateOnScroll from '@/views/AnimateOnScroll.vue'
import practice from '@/views/practice.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/fullpagescroll',
    name: 'FullPageScroll',
    component: FullPageScroll
  },
  {
    path: '/aos',
    name: 'AOS',
    component: AOS
  },
  {
    path: '/main-scroll',
    name: 'MainScroll',
    component: MainScroll
  },
  {
    path: '/animate-on-scroll',
    name: 'AnimateOnScroll',
    component: AnimateOnScroll
  },
  {
    path: '/practice',
    name: 'practice',
    component: practice
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
