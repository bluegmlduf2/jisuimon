<template>
  <div class="container-fluid">
    <router-view class="card" name="Card" :posts="posts"/>
    <router-view class="post" name="Post" :posts="posts"/>
  </div>
</template>

<script>
// import Card from './Card.vue'
import postDatas from '@/assets/posts.js';

export default {
  name:"Main",
  components:{
    // Card:Card
  },
  data() {
    return {
      loading:false,
      posts:postDatas
    }
  },
  methods:{
    fetchData(){
      this.posts = postDatas;
      this.loading = true;
    }
  },
  // 데이터 초기화(페치)에 사용함 mounted보다 먼저실행됨
  befroecreated(){
    this.fetchData();
  }
}
</script>

<style>
@media (max-width: 576.98px){
  .container-fluid{
    padding-top: 80px;
  }
}

@keyframes slide {
 from {
  bottom: 0;
 }
 to {
  bottom: 12px;
 }
}
.card{
  transition: transform 250ms;
}
.card:hover {
 transform: translateY(-10px);
 /* offset-x | offset-y | blur-radius | spread-radius | color */
 box-shadow: 45px 45px 40px -30px rgb(240, 240, 245);
}
</style>