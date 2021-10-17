<template>
  <div class="container-fluid">
    <!-- Main -->
    <router-view class="card" name="Card" :posts="posts"/>
    <!-- Post -->
    <router-view class="post" name="Post" :posts="posts"/>
    <router-view class="comment" name="Comment"/>
  </div>
</template>

<script>
// import Card from './Card.vue'
import postDatas from '@/assets/js/posts.js';

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
/* 메인 레이아웃 css */
@media (max-width: 576.98px){
  .container-fluid{
    padding-top: 80px;
  }
}

/* Card 애니메이션*/
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

/* Post,Comment 공통 레이아웃 */
@media (min-width: 992px){
  /* 넓이가 992px 이상 여백추가*/
  .postCont, .commentCont{
    text-align: left;
    padding-left:160px;
    padding-right:160px;
  }
}
</style>