<template>
  <div class="container-fluid">
    <Card :posts="posts"/>
  </div>
</template>

<script>
import Card from './Card.vue'
import postDatas from '@/assets/posts.js';

export default {
  name:"Main",
  components:{
    Card:Card
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
</style>