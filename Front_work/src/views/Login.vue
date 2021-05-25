<template>
  <div b-container cotainer-fluid>
    <div id="bg" class="carousel slide" :style="{ width: windowWidth }" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="4000">
          <img src="https://www.themoviedb.org/t/p/w1066_and_h600_bestv2/2nbKZ5RWFSvjq5IGVRcz8kAolmw.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbwBmBj%2FbtqzlkqsFRT%2FDdWgcmONokKV2w3e5JGnZ0%2Fimg.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcfyMPk%2FbtqzjJSVxwa%2F585yMvmx8k0morUKKgEkB1%2Fimg.jpg" class="d-block w-100" alt="...">
        </div>
      </div>
    </div>
    <img style="color: #f1f1f1; font-size: 7rem; width: 20rem;" src="../assets/logo_transparent.png">
    <div class="login">
      <el-card class="login-card pb-1">
        <span style="color: #f1f1f1; opacity: 0.7;">"나의 죽음이 나의 삶보다 가취 있기를"</span><br><br>
        <span style="color: #f1f1f1; opacity: 0.7;">-영화 '조커' 中</span><br>
        <el-form
          class="login-form mt-3"
          :model="credentials"
          :rules="rules"
          ref="form"
          @submit.native.prevent="login(credentials)"
        >
          <el-form-item prop="username">
            <el-input v-model="credentials.username" placeholder="아이디" prefix-icon="fas fa-user"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="credentials.password"
              placeholder="비밀번호"
              type="password"
              prefix-icon="fas fa-lock"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              id="login-button"
              type="primary"
              native-type="submit"
              block
            ><span style="color: rgba(255, 255, 255, 0.82);">로그인</span></el-button>
          </el-form-item>
          <h6 class="signup-router text-secondary p-0" @click="$router.push({ name: 'Signup'})">회원가입</h6>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
  export default {
    name: 'Login',
    data() {
      return {
        credentials: {
          username: '',
          password: '',
        },
        windowWidth: parseInt(screen.availWidth)+"px",
        rules: {
          username: [
            {
              required: true,
              message: "Username is required",
              trigger: "blur"
            },
          ],
          password: [
            { required: true, message: "Password is required", trigger: "blur" },
          ]
        }
      }
    },
    methods: {
      ...mapActions([
        'login',
      ]),
    }
  }
</script>
<style>
#bg {
  position: fixed; 
  z-index: -1;
  top: 0; 
  left: 0; 
  margin: auto;
}
.container {
  padding: 16px;
}

.login {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

#login-button {
  width: 100%;
  margin-top: 40px;
  padding: 14px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  transition: 0.5s;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.82);
}
.login-card{
  background-color: rgba(0, 0, 0, 0.9);
  border-color: rgba(0, 0, 0, 0.9);;
}
.login-form {
  width: 290px;
}
.signup-router {
  margin-top: 10px;
  font-size: 13px;
  cursor: pointer;
}
</style>

<style lang="scss">
$teal: rgba(71, 63, 113, 0.8);
#login-button {
  background: $teal;
  border-color: $teal;

  &:hover,
  &.active,
  &:focus {
    background: lighten($teal, 20);
    border-color: lighten($teal, 20);
  }
}
.login .el-input__inner:hover {
  border-color: $teal;
}
.login .el-input__prefix {
  background: rgb(238, 237, 234);
  left: 0;
  height: calc(100% - 2px);
  left: 1px;
  top: 1px;
  border-radius: 3px;
  .el-input__icon {
    width: 30px;
  }
}
.login .el-input input {
  padding-left: 35px;
}
.login .el-card {
  padding-top: 0;
  padding-bottom: 30px;
}
h2 {
  font-family: "Open Sans";
  letter-spacing: 1px;
  font-family: Roboto, sans-serif;
  padding-bottom: 20px;
  color: rgba(255, 255, 255, 0.82);
}
a {
  color: $teal;
  text-decoration: none;
  &:hover,
  &:active,
  &:focus {
    color: lighten($teal, 7);
  }
}
.login .el-card {
  width: 340px;
  display: flex;
  justify-content: center;
}
</style>