<template>
  <div class="AOS">
    <h1>AOS Page</h1>
    <div data-aos="fade-up">fade up</div>
    <div data-aos="fade-down">fade down</div>
    <div data-aos="fade-right">fade-right </div>
    <div class="margin-top" data-aos="zoom-in-up" data-aos-duration="1000">
      <img src="https://picsum.photos/seed/picsum/200/300" alt="">
    </div>
    https://michalsnik.github.io/aos/
  </div>
</template>

<script>
export default {
  name: 'AOS'
}
</script>

<style>
  .margin-top {
    margin: 10%;
  }
</style>