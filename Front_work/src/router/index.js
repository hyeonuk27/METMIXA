import Vue from 'vue'
import VueRouter from 'vue-router'
import Profile from '@/views/Profile.vue'
import Signup from '@/views/Signup.vue'
import Login from '@/views/Login.vue'
import Main from '@/views/Main.vue'
import Detail from '@/views/Detail.vue'
import ReviewComment from '@/views/ReviewComment.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  {
    path: '/detail',
    name: 'Detail',
    component: Detail,
  },
  {
    path: '/comment',
    name: 'Comment',
    component: ReviewComment,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router


// 로그인 한 상태 -> Main, Detail, Profile
// 로그아웃 한 상태 -> Login, Signup

// form - 어디에서 왔는지, to - 어디로 갔는지, next - to로 가기
router.beforeEach((to, from, next) => {

  // 1-1. 로그인이 필요한 컴포넌트
  const authPages = [
    'Main',
    'Profile',
    'Detail',
    'Comment',
  ]
  // 1-2. 로그아웃이 필요한 컴포넌트
  const publicPages = [
    'Login',
    'Signup',
  ]

  // 2. 
  // 가려고 하는 곳(to)이 로그인이 필요한 곳인지 여부를 체크
  const authRequired = authPages.includes(to.name)
  // 가려고 하는 곳이 로그인이 필요하지 않은 곳이지 여부를 체크
  const authNotRequired = publicPages.includes(to.name)
  // 로그인이 되어있는지 여부를 체크
  const isLoggedin = localStorage.getItem('jwt') ? true : false

  //3 .
  // 3-1. 만약 로그인이 필요한 컴포넌트인데 로그인이 안되어 있는 경우에 강제로 가려하면
  if (authRequired && !isLoggedin) {
    // 로그인 할 수 있도록 가드 -> Login 컴포넌트로 보내기(redirect 느낌)
    next({ name: 'Login' })
  } else if (authNotRequired && isLoggedin) {
    next({ name: 'Main' })
  } else {
    next()
  }

  if ((from.name === 'Main' && to.name === 'Login') || (from.name === 'Login' && to.name === 'Signup') || (from.name === 'Signup' && to.name === 'Login') || (from.name === 'Comment' && to.name === 'Detail')) {
    next()
    window.location.reload()
  }
})