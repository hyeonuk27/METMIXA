<template>
  <div class="FullPage">
    <full-page ref="fullpage" :options="options" id="fullpage">
    <div class="section">
      <h1>Wow this is first section!</h1>
      <img src="https://picsum.photos/seed/picsum/200/300" alt="">
    </div>
    <div class="section">
      Second section ...
      <img src="https://picsum.photos/seed/picsum/200/300" alt="">
    </div>
    <div class="section">
      Third section ...
      <img src="https://picsum.photos/seed/picsum/200/300" alt="">
    </div>
    </full-page>
  </div>
</template>

<script>
export default {
  name: 'FullPageScroll'
}
</script>

<style>

</style>