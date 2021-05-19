<template>
  <div>
    <section id="app">
      <h1>Vue.js slider</h1>
      <section>
      <h2>Basic example</h2>
      <article>
        <div>
          <label>Slide value :</label>
          <input type="number" v-model="basicSlideValue"/>
        </div>
        <div>
          <label>Min :</label>
          <input type="number" v-model="basicSlideOptions.min" placeholder="0 (default)"/>
        </div>
        <div>
          <label>Max :</label>
          <input type="number" v-model="basicSlideOptions.max" placeholder="100 (default)"/>
        </div>
        <div>
          <label>Step :</label>
          <input type="number" v-model="basicSlideOptions.step" placeholder="1 (default)"/>
        </div>
        <div>
          <label>Number of pips :</label>
          <input type="number" v-model="basicSlideOptions.nbPips" placeholder="48 (default)"/>
        </div>
        <div>
          <label>Color :</label>
          <input type="color" v-model="basicSlideOptions.color"/>
        </div>
        </article>
        <vue-slider v-model="basicSlideValue" :options="basicSlideOptions" class="slider">
        </vue-slider>
      </section>
    </section>
  </div>
</template>

<script>
export default {
  name: 'MainScroll',
}

// Vue.component('vue-slider', {
//   template: `
//     <section @mousewheel.prevent="scroll" @click="e => slideTo(getClosestValue(e))" @mouseover="e => hoverValue = getClosestValue(e)" @mouseout="hoverValue = null" ref="slider">
//       <div class="pips">
//         <span class="value-cursor" :style="'left: ' + (cursorPosition - 10) + 'px; border-top-color: ' + (options.color || 'black') + ';'"></span>
//         <span class="value-displayer" :style="'left: ' + (cursorPosition - 25) + 'px;'" ref="valueDisplayer">
//           <slot :value="slideValue">
//             {{slideValue}}
//           </slot>
//         </span>
//         <span v-for="(pip, index) in pips" :key="index" class="pip" :class="getActive(index)" :style="'background: ' + (options.color || 'black') + ';'" :ref="getActive(index)"></span>
//       </div>
//     </section>
//   `,
  /*
  Props :
    - value (Number ; required) : v-model
    - options (Object) : slider's options. Params are :
      - min (Number ; default : 0) : minimum slider's value
      - max (Number ; default : 100) : maximum slider's value
      - step (Number ; default : 1) : step between each value
      - nbPips (Number ; default : 48) : number of pips in the slider
      - lockedSteps (Array) : specific steps ([10, 12, 15, 20] for example). If it's set, min become its first value, max become it's last value and step define the transition's speed between each step
      - color (String ; default : black) : pips' and cursor's color
      - interval (Number ; default : 1) : time between each step (in ms)
  */
//   props: {
//     value: {
//       required: true
//     },
//     options: {
//       type: Object,
//       default: () => { return {} }
//     }
//   },
//   data () {
//     return {
//       pips: [],
//       values: [],
//       transition: false,
//       cursorPosition: 0,
//       hoverValue: null,
//       windowWidth: 0
//     }
//   },
//   computed: {
//     // Set up v-model
//     slideValue: {
//       get () {
//         return this.value * 1
//       },
//       set (value) {
//         this.$emit('input', value)
//       }
//     },
//     // Check if lockedSteps has been setted, else check for min, else set it to default
//     min () {
//       if (this.options.lockedSteps && this.options.lockedSteps.length > 0) {
//         return [...this.options.lockedSteps].sort((a, b) => {
//           return a * 1 - b * 1
//         })[0]
//       } else if (this.options.min) {
//         return this.options.min * 1
//       } else {
//         return 0
//       }
//     },
//     // Check if lockedSteps has been setted, else check for max, else set it to default
//     max () {
//       if (this.options.lockedSteps && this.options.lockedSteps.length > 0) {
//         return [...this.options.lockedSteps].sort((a, b) => {
//           return a * 1 - b * 1
//         })[this.options.lockedSteps.length - 1]
//       } else if (this.options.max) {
//         return this.options.max * 1
//       } else {
//         return 100
//       }
//     },
//     // Check if nbPips has been setted, else set it to default
//     nbPips () {
//       return this.options.nbPips * 1 || 48
//     },
//     // Check if step has been setted and is valid, else set it to default
//     step () {
//       if (this.options.step && this.options.step * 1 > 0) {
//         return this.options.step * 1
//       } else {
//         return 1
//       }
//     },
//     // Check if interval has been setted and is valid, else set it to default
//     interval () {
//       if (this.options.cursorSpeed && this.options.cursorSpeed >= 0) {
//         return this.options.interval
//       } else {
//         return 1
//       }
//     }
//   },
//   methods: {
//     initialize () {
//       // Init pips
//       this.pips = []
//       for (let i = 0; i < this.nbPips; i++) {
//         this.pips.push('')
//       }
//       // Store all possible values
//       if (this.options.lockedSteps) {
//         this.values = [...this.options.lockedSteps].sort((a, b) => {
//           return a * 1 - b * 1
//         })
//       } else {
//         this.values = []
//         for (let i = 0; i <= Math.floor((this.max - this.min) / this.step); i++) {
//           i === 0 ? this.values.push(this.min) : this.values.push(this.values[i - 1] + this.step)
//         }
//       }
//       // Init cursor and active pip
//       if (this.options.lockedSteps) {
//         this.slideTo(this.min)
//       } else if (this.slideValue < this.min) {
//         this.slideTo(this.min)
//       } else if (this.slideValue > this.max) {
//         this.slideTo(this.max)
//       } else {
//         this.slideTo(this.slideValue)
//       }
//       // Invalid props handler
//       if (this.min > this.max) {
//         console.warn(`Warning : the slider's min (${this.min}) is higher than its max (${this.max}).`)
//       }
//       if (this.step > this.values.length && !this.options.lockedSteps) {
//         console.warn(`Warning : the slider's step (${this.options.step || 1}) is too high (it should not be higher than ${this.values.length} according the given values).`)
//       }
//     },
//     // Mousewheel handler
//     scroll (e) {
//       if (!this.transition) {
//         const index = this.values.indexOf(this.slideValue)
//         if (index >= 0) {
//           if (e.deltaY > 0 && index !== 0) {
//             this.slideTo(this.values[index - 1])
//           } else if (e.deltaY < 0 && index !== this.values.length - 1) {
//             this.slideTo(this.values[index + 1])
//           }
//         } else {
//           this.slideValue = this.values[0]
//         }
//       }
//     },
//     // Get active pip and its neighbours based on slide value
//     getActive (index) {
//       const currentPip = Math.round((this.slideValue - this.min) * (this.nbPips - 1) / (this.max - this.min))
//       const hoveredPip = this.hoverValue !== null ? Math.round((this.hoverValue - this.min) * (this.nbPips - 1) / (this.max - this.min)) : null
//       if (index === currentPip) {
//         return 'active'
//       } else if (index === currentPip + 1 || index === currentPip - 1 || index === hoveredPip) {
//         return 'active-neighbour'
//       }
//     },
//     // Set up interval in order to slide smoothly
//     slideTo (to) {
//       if (!this.transition) {
//         this.transition = true
//         const interval = setInterval(() => {
//           if (this.slideValue < to && this.slideValue < this.max) {
//             this.slideValue += this.step
//           } else if (this.slideValue > to && this.slideValue > this.min) {
//             this.slideValue -= this.step
//           } else {
//             clearInterval(interval)
//             this.transition = false
//           }
//           this.getCursorPosition()
//         }, this.interval)
//       }
//     },
//     // Get cursor's position based on active pip offset
//     getCursorPosition () {
//       if (this.$refs.active && this.$refs.valueDisplayer) {
//         const active = this.$refs.active[0] || this.$refs.active
//         this.cursorPosition = active.offsetLeft + active.offsetWidth / 2
//       } else {
//         this.cursorPosition = 0
//       }
//     },
//     // Mouse click & hover handler
//     getClosestValue (e) {
//       // Get slider's percent of the click's location
//       const percent = Math.round(e.layerX * 100 / (this.$refs.slider.offsetWidth))
//       // Get associated value
//       const value = Math.round(percent * (this.max - this.min) / 100) + this.min
//       return this.values.reduce((prev, current) => {
//         return (Math.abs(current - value) < Math.abs(prev - value) ? current : prev)
//       })
//     },
//     // Get window width
//     resizeHandler () {
//       this.windowWidth = window.innerWidth
//     }
//   },
//   watch: {
//     // Check if slide value does not exceed min or max
//     slideValue (newVal, oldVal) {
//       if (newVal > this.max) {
//         this.slideTo(this.max)
//       } else if (newVal < this.min) {
//         this.slideTo(this.min)
//       } else {
//         this.slideTo(this.slideValue)
//       }
//     },
//     // Each time locked steps change, reset slide value to its first value
//     options: {
//       handler () {
//         if (this.options.step && this.options.step <= 0) {
//           console.warn('Warning, the step is inferior or equal to 0. It has been setted to its default value : 1.')
//         }
//         this.initialize()
//       },
//       deep: true
//     },
//     // Update cursor's position on resize
//     windowWidth () {
//       this.getCursorPosition()
//     }
//   },
//   created () {
//     // Update window width
//     window.addEventListener('resize', this.resizeHandler, false)
//   },
//   mounted () {
//     this.initialize()
//   },
//   beforeDestroyed () {
//     window.removeEventListener('resize', this.resizeHandler, false)
//   }
// })

// new Vue({
//   el: '#app',
//   data: {
//     basicSlideValue: 50,
//     basicSlideOptions: {
//       color: '#000000'
//     },
//     slotSlideValue: 50,
//     lockedSlideValue: 0,
//     lockedSlideOptions: {
//       lockedSteps: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
//     }
//   }
// })

</script>



<style>
  /* .pips {
  display: flex;
  position: relative;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  & .value-cursor {
    transition: 0.3s;
    position: absolute;
    top: -15px;
    display: block;
    height: 0;
    width: 0;
    border: 10px solid transparent;
  }
  & .value-displayer {
    transition: 0.3s;
    position: absolute;
    top: 100px;
    display: block;
    width: 50px;
    text-align: center
  }
  & .pip {
    margin: 5px;
    display: block;
    width: 20px;
    transition: 0.3s;
    height: 50px;
    border-radius: 10px;
    &.active-neighbour {
      height: 75px;
    }
    &.active {
      height: 100px!important;
    }
  }
}

// Pen specific CSS
body {
  font-family: "Helvetica Neue","Helvetica","Arial",sans-serif;
  color: rgba(0, 0, 0, 0.8);
  background: #f0f0f6;
}

article {
  display: flex;
  justify-content: space-around;
  &>div {
    display: flex;
    flex-direction: column;
    &>label {
      color: rgba(0, 0, 0, 0.7);
      margin-bottom: 5px;
      font-size: 0.9rem;
    }
    &>input[type=number] {
      border: none;
      border-bottom: 1px solid black;
      padding-bottom: 5px;
      background: none;
      transition: 0.3s;
      &:focus {
        border-bottom: 2px solid black;
        outline: none;
      }
    }
  }
}

.slider {
  margin: 50px;
} */
</style>