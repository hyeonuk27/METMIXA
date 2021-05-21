<template>
  <div>
    <!-- 유저 이름, 닉네임, 사진 -->
    <UserInfo/>
    <!-- 유저 정보 변경을 위한 modal-->
    <!-- v-for로 반복 돌리기 -->
    <PhotoTicket
    v-for="(photoTicket, idx) in photoTickets"
    :key="idx"
    />
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data: function () {
    return {
        photoTickets: [],
        pageNum: 1,
    }
  },
  methods: {
    getMovies: function () {
      axios({
        method: 'get',
        // 장고한테 요청
        url: 'http://127.0.0.1:8000/api/v1/phototickets/',
        params: {
          page_num = this.pageNum,
        },
      })
      .then((response)=>{
        console.log(response.data)
        // movie에 대한 JSON
        this.photoTickets.push(...response.data)
        this.pageNum += 1
      })
    },
    checkBottom: function () {
      const {scrollTop, clientHeight, scrollHeight} = document.documentElement
      if (scrollHeight - scrollTop === clientHeight) {
        this.getMovies()
      }
    }
  },
  created: function () {
    console.log(this.url)
    this.getMovies()
    document.addEventListener('scroll', this.checkBottom)
  }
}
</script>

<style>

</style>