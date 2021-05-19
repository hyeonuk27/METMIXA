<template>
  <div>
    <div class="section">
      <img :src="selectedImage1" class="heartbeat" @wheel="wheelmove" alt="">
      <img :src="selectedImage2" class="heartbeat" @wheel="wheelmove" alt="">
      <img :src="selectedImage3" class="heartbeat" @wheel="wheelmove" alt="">
      <img :src="selectedImage4" class="heartbeat" @wheel="wheelmove" alt="">
      <img :src="selectedImage5" class="heartbeat" @wheel="wheelmove" alt="">
    </div>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'practice',
  data: function () {
    return {
      images: [
        "https://picsum.photos/id/1/200/300",
        "https://picsum.photos/id/2/200/300",
        "https://picsum.photos/id/3/200/300",
        "https://picsum.photos/id/4/200/300",
        "https://picsum.photos/id/5/200/300",
        "https://picsum.photos/id/211/200/300",
        "https://picsum.photos/id/212/200/300",
        "https://picsum.photos/id/213/200/300",
        "https://picsum.photos/id/214/200/300",
        "https://picsum.photos/id/215/200/300",

      ],
      selectedImage1: 'https://picsum.photos/id/227/200/300',
      selectedImage2: 'https://picsum.photos/id/223/200/300',
      selectedImage3: 'https://picsum.photos/id/40/200/300',
      selectedImage4: 'https://picsum.photos/id/1/200/300',
      selectedImage5: 'https://picsum.photos/id/2/200/300',
    }
  },
  methods: {
    // 마우스 휠 움직이면 이미지 바뀌는 거
    // 마우스 휠 파워크기가 1이면 한장씩 옮기고
    // 5보다 크면 5장 한 번에 바꾼다.
    wheelmove: function(e) {
      if (e.wheelDeltaY < 0) {
        console.log(e.value)
        e.preventDefault()
        this.selectedImage1 = this.images[0]
        this.selectedImage2 = this.images[1]
        this.selectedImage3= this.images[2]
        this.selectedImage4 = this.images[3]
        this.selectedImage5 = this.images[4]
      } else if (e.wheelDeltaY > 0) {
        e.preventDefault()
        this.selectedImage1 = this.images[_.random(9)]
        this.selectedImage2 = this.images[_.random(9)]
        this.selectedImage3= this.images[_.random(9)]
        this.selectedImage4 = this.images[_.random(9)]
        this.selectedImage5 = this.images[_.random(9)]
      }
  }
  },

}
</script>

<style>
  img {
    margin: 10px;
  }
  .wobble-hor-bottom {
    -webkit-animation: wobble-hor-bottom 0.8s both;
            animation: wobble-hor-bottom 0.8s both;
  }
  @-webkit-keyframes wobble-hor-bottom {
    0%,
    100% {
      -webkit-transform: translateX(0%);
              transform: translateX(0%);
      -webkit-transform-origin: 50% 50%;
              transform-origin: 50% 50%;
    }
    15% {
      -webkit-transform: translateX(-30px) rotate(-6deg);
              transform: translateX(-30px) rotate(-6deg);
    }
    30% {
      -webkit-transform: translateX(15px) rotate(6deg);
              transform: translateX(15px) rotate(6deg);
    }
    45% {
      -webkit-transform: translateX(-15px) rotate(-3.6deg);
              transform: translateX(-15px) rotate(-3.6deg);
    }
    60% {
      -webkit-transform: translateX(9px) rotate(2.4deg);
              transform: translateX(9px) rotate(2.4deg);
    }
    75% {
      -webkit-transform: translateX(-6px) rotate(-1.2deg);
              transform: translateX(-6px) rotate(-1.2deg);
    }
  }
  @keyframes wobble-hor-bottom {
    0%,
    100% {
      -webkit-transform: translateX(0%);
              transform: translateX(0%);
      -webkit-transform-origin: 50% 50%;
              transform-origin: 50% 50%;
    }
    15% {
      -webkit-transform: translateX(-30px) rotate(-6deg);
              transform: translateX(-30px) rotate(-6deg);
    }
    30% {
      -webkit-transform: translateX(15px) rotate(6deg);
              transform: translateX(15px) rotate(6deg);
    }
    45% {
      -webkit-transform: translateX(-15px) rotate(-3.6deg);
              transform: translateX(-15px) rotate(-3.6deg);
    }
    60% {
      -webkit-transform: translateX(9px) rotate(2.4deg);
              transform: translateX(9px) rotate(2.4deg);
    }
    75% {
      -webkit-transform: translateX(-6px) rotate(-1.2deg);
              transform: translateX(-6px) rotate(-1.2deg);
    }
  }
  
  @-webkit-keyframes heartbeat{from{-webkit-transform:scale(1);transform:scale(1);-webkit-transform-origin:center center;transform-origin:center center;-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}10%{-webkit-transform:scale(.91);transform:scale(.91);-webkit-animation-timing-function:ease-in;animation-timing-function:ease-in}17%{-webkit-transform:scale(.98);transform:scale(.98);-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}33%{-webkit-transform:scale(.87);transform:scale(.87);-webkit-animation-timing-function:ease-in;animation-timing-function:ease-in}45%{-webkit-transform:scale(1);transform:scale(1);-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}}@keyframes heartbeat{from{-webkit-transform:scale(1);transform:scale(1);-webkit-transform-origin:center center;transform-origin:center center;-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}10%{-webkit-transform:scale(.91);transform:scale(.91);-webkit-animation-timing-function:ease-in;animation-timing-function:ease-in}17%{-webkit-transform:scale(.98);transform:scale(.98);-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}33%{-webkit-transform:scale(.87);transform:scale(.87);-webkit-animation-timing-function:ease-in;animation-timing-function:ease-in}45%{-webkit-transform:scale(1);transform:scale(1);-webkit-animation-timing-function:ease-out;animation-timing-function:ease-out}}

  .heartbeat{-webkit-animation:heartbeat 2s ease-in-out 1 both;animation:heartbeat 2s ease-in-out 1 both}
</style>