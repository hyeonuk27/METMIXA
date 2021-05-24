<template>
  <div>
    <header id="header">
      <span class="avatar">
        <img v-if="image" :src="image" alt="" />
        <img v-else src="@/assets/default_profile.jpg" alt="" />
      </span>
      <h2>{{ nickname }}님의 공간</h2>
    </header>
  </div>
</template>

<script>
export default {
  name: "UserInfo",
  props: {
    nickname: {
      type: String,
    },
    image: {
      type: String,
    },
  }
}
</script>

<style>
#header {
  text-align: center;
  padding: 6em 0 4em 0;
}

h2 {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 200;
}

.avatar {
  border-radius: 100%;
  display: inline-block;
  margin: 0 0 2em 0;
  padding: 0.5em;
  border: solid 1px rgba(255, 255, 255, 0.25);
  background-color: rgba(255, 255, 255, 0.075);
}

#header .avatar img {
  border-radius: 100%;
  display: block;
  width: 10em;
}

@media screen and (max-width: 1280px) {
  #header {
    padding: 4em 0 2em 0;
  }
}
</style>