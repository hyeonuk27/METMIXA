<template>
  <div b-container cotainer-fluid>
    <div id="bg" class="carousel slide" :style="{ width: windowWidth }" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="4000">
          <img src="https://www.themoviedb.org/t/p/w1066_and_h600_bestv2/2nbKZ5RWFSvjq5IGVRcz8kAolmw.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://www.themoviedb.org/t/p/w1066_and_h600_bestv2/nyuzfjAbuSel6dVKY4zFo95ugUf.jpg
" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="4000">
          <img src="https://www.themoviedb.org/t/p/w1066_and_h600_bestv2/27IQ08XLxw2Gaj5zoOmJWmq4nNy.jpg" class="d-block w-100" alt="...">
        </div>
      </div>
    </div>
    <div class="signup">
      <el-card class="signup-card pb-1">
        <h2>Signup</h2>
        <el-form
          class="signup-form"
          :model="credentials"
          :rules="rules"
          ref="form"
          @submit.native.prevent="onUpload"
        >
          <el-form-item prop="nickname">
            <el-input v-model="credentials.nickname" placeholder="Nickname" prefix-icon="fas fa-user"></el-input>
          </el-form-item>
          <el-form-item prop="username">
            <el-input v-model="credentials.username" placeholder="Username" prefix-icon="fas fa-user"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="credentials.password"
              placeholder="Password"
              type="password"
              prefix-icon="fas fa-lock"
            ></el-input>
          </el-form-item>
          <el-form-item prop="passwordCofirmation">
            <el-input
              v-model="credentials.passwordConfirmation"
              placeholder="Password Cofirmation"
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
              class="signup-button"
              type="primary"
              native-type="submit"
              block
            ><span style="color: rgba(255, 255, 255, 0.82);">Signup</span></el-button>
          </el-form-item>
          <h6 class="greeting text-secondary">METMIXA는 당신을 기다립니다.</h6>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
// import default_profile from '@/assets/default_profile.jpg'
// console.log(typeof('@/assets/default_profile.jpg'))
// const imageFile = new XMLHttpRequest()
// imageFile.open("GET", "@/assts/default_profile.jpg", false)
// console.log(imageFile)

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        nickname: '',
        username: '',
        password: '',
        passwordConfirmation: '',
        // image: '',
      },
      windowWidth: parseInt(window.innerWidth)+"px",
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
      }
    }
  },
  methods: {
    ...mapActions([
      'signup',
    ]),
    goProfile() {
      this.$router.push({name: 'Profile'})
    },
    onUpload: function () {
      // console.log(this.credentials.image)
      // let imageData = new FormData()
      // imageData.append('image', this.image)
      // this.credentials.image = imageData
      // for (var value of this.credentials.image.values()) {
      // console.log(value);
      // }
      // console.log(this.credentials.image)
      this.signup(this.credentials)
    }
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
.signupBtn:hover {
  opacity: 0.6;
}
.container {
  padding: 16px;
}

.signup {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 8rem;
}

.signup-button {
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
.el-button--primary {
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