<template>
  <div id="photo_ticket_layer" class="d-flex justify-content-center p-1 m-0">
    <div class="photo_ticket">
      <img id="image" :src="photoTicket.poster_path" class="card-img-top" alt="...">
      <div>
        <p>{{ photoTicket.message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PhotoTicket",
  props: {
    photoTicket: {
      type: Object,
    }
  }
}
</script>

<style>
.photo_ticket:hover {
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.25), 0 0 0.5em 0 #FF6382;
}

.photo_ticket p {
  text-align: start;
  color: rgba(255, 255, 255, 0.82);
  display: block;
  margin: 0.5em;
}

img {
  width: 100%;
}

.photo_ticket {
  transition: all 0.2s ease;
  border-bottom: none;
  display: block;
  width: 100%;
  height: 100%;
  margin: 0;
  text-align: center;
  border-radius: 4px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.25);
  background-color: rgba(255, 255, 255, 0.075);
  cursor: pointer;
  outline: 0;
  overflow: hidden;
}

</style>