<template>
  <div b-container cotainer-fluid>
    <div id="bg" class="carousel slide" :style="{ width: windowWidth }" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="4000">
          <img src="https://i.pinimg.com/originals/a4/04/3e/a4043e1c09a7c1cdb94f6e9a84c2e507.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://pds.joins.com/news/component/htmlphoto_mmdata/201701/09/htm_20170109115141307904.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://an2-img.amz.wtchn.net/image/v2/22ea1094cfdf39a5fa3d168e5ae89343.jpg?jwt=ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlKaVlXTnJaM0p2ZFc1a0lqcDdJbklpT2pJMU5Td2laeUk2TWpVMUxDSmlJam95TlRWOUxDSmpjbTl3SWpwMGNuVmxMQ0pvWldsbmFIUWlPakV3T0RBc0luQmhkR2dpT2lJdmRqSXZjM1J2Y21VdmFXMWhaMlV2TVRZeE5UZ3pNakUzTnpJNU5UWXlNelF4T1NJc0luRjFZV3hwZEhraU9qZ3dMQ0ozYVdSMGFDSTZNVGt5TUgwLjB1SmN4WnVrUTVFNDFYVURkeEtyNk1RTzA2a25RWUxiQmRWYzBGNGpuQm8" class="d-block w-100" alt="...">
        </div>
      </div>
    </div>
    <img style="color: #f1f1f1; font-size: 7rem; width: 20rem;" src="../assets/logo_transparent.png">
    <div class="signup">
      <el-card class="signup-card pb-1">
        <span style="color: #f1f1f1; opacity: 0.7;">"우린 어디쯤 있는 거지?"</span><br>
        <span style="color: #f1f1f1; opacity: 0.7;">"그냥 흘러가는 대로 가보자"</span><br><br>
        <span style="color: #f1f1f1; opacity: 0.7;">-영화 '라라랜드' 中</span><br>
        <el-form
          class="signup-form mt-3"
          :model="credentials"
          :rules="rules"
          ref="form"
          @submit.native.prevent="isValid"
        >
          <el-form-item prop="nickname">
            <el-input v-model="credentials.nickname" placeholder="닉네임" prefix-icon="fas fa-user"></el-input>
          </el-form-item>
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
          <el-form-item prop="passwordCofirmation">
            <el-input
              v-model="credentials.passwordConfirmation"
              placeholder="비밀번호 확인"
              type="password"
              prefix-icon="fas fa-lock"
            ></el-input>
          </el-form-item>
          <!-- <el-form-item prop="image">
            <el-input
              v-model="credentials.image"
              placeholder="image"
              type="file"
              accept="image/*"
              prefix-icon="el-icon-picture-outline"
            ></el-input>
            <v-file-input v-model="credentials.image"></v-file-input>
          </el-form-item> -->
          <el-form-item>
            <el-button
              id="signup-button"
              type="primary"
              native-type="submit"
              block
            ><span style="color: rgba(255, 255, 255, 0.82);">회원가입</span></el-button>
          </el-form-item>
          <h6 class="greeting text-secondary">METMIXA는 당신을 기다립니다.</h6>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import swal from 'sweetalert'

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        nickname: '',
        username: '',
        password: '',
        passwordConfirmation: '',
      },
      windowWidth: parseInt(screen.availWidth)+"px",
      rules: {
        nickname: [
          {
            required: true,
            message: "Nickname is required",
            trigger: "blur"
          },
        ],
        username: [
          {
            required: true,
            message: "Username is required",
            trigger: "blur"
          },
        ],
        password: [
          { required: true, message: "Password is required", trigger: "blur" },
        ],
        passwordConfirmation: [
          { required: true, message: "Password Confirmation is required", trigger: "blur" },
        ]
      },
    }
  },
  methods: {
    ...mapActions([
      'signup',
    ]),
    goProfile() {
      this.$router.push({name: 'Profile'})
    },
    isValid: function () {
      if (this.credentials.nickname === '' || this.credentials.username === '' || this.credentials.password === '' || this.credentials.passwordConfirmation == '') {
        swal ("필수 정보를 모두 입력해주세요.", {
          dangerMode: true,
        })
      } else {
        this.signup(this.credentials)
      }
    }
  },
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
.signup {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
#signup-button {
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
.signup-card{
  background-color: rgba(0, 0, 0, 0.9);
  border-color: rgba(0, 0, 0, 0.9);;
}
.signup-form {
  width: 290px;
}
.greeting {
  margin-top: 10px;
  font-size: 13px;
}
</style>

<style lang="scss">
$teal: rgba(71, 63, 113, 0.8);
#signup-button {
  background: $teal;
  border-color: $teal;

  &:hover,
  &.active,
  &:focus {
    background: lighten($teal, 20);
    border-color: lighten($teal, 20);
  }
}
.signup .el-input__inner:hover {
  border-color: $teal;
}
.signup .el-input__prefix {
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
.signup .el-input input {
  padding-left: 35px;
}
.signup .el-card {
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
.signup .el-card {
  width: 340px;
  display: flex;
  justify-content: center;
}
</style>