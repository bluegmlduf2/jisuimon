<template>
  <div class="post-list-cont">
    <div class="post-list-search" >
      <h6>Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum, laudantium velit </h6>
      <input class="form-control mr-sm-4" id="searcPost" type="text" placeholder="食材を入力してください">
    </div>
    <!-- <div class="post-list" v-for="i in 8" :key="i"> -->
    <div class="post-list" >
      <router-link to="#" class="post-list-title">
        <h2>Lorem ipsum dolor sit amet consectetur adipisicing elit. Deserunt illo ab aspernatur numquam. Reiciendis hic ratione repudiandae unde aliquam vel numquam nemo eaque, nihil consequatur itaque</h2>
      </router-link>
      <p class="post-list-content">
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Rerum, numquam. Doloribus a repudiandae blanditiis ex accusantium cumque culpa nam, mollitia dolor, expedita, fugit reprehenderit veniam praesentium quod enim cupiditate dolorem!
        Qui porro quas molestiae assumenda obcaecati molestias, modi error temporibus dolorem recusandae adipisci sit similique aliquid ab, deserunt corrupti debitis, tenetur vitae quisquam quis! Odio, maxime. Vero rerum libero velit.
      </p>
      <div class="post-list-subinfo">
        <span class="post-list-date">2022.11.11</span>
        <span class="post-list-comment"> 0개의댓글</span>
      </div>
    </div>
    <div class="post-list" >
      <router-link to="#" class="post-list-title">
        <h2>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Dolor quia unde quaerat nemo, assumenda neque. Deleniti placeat quaerat sequi fuga, ex fugit distinctio laudantium hic, impedit maxime quod dolor officia.</h2>
      </router-link>
      <p class="post-list-content">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. 
      </p>
      <div class="post-list-subinfo">
        <span class="post-list-date">2022.11.11</span>
        <span class="post-list-comment"> 0개의댓글</span>
      </div>
    </div>
  </div>
</template>

<script>
import common from "@/assets/js/common.js";

export default {
  name: "PostList",
  mixins: [common],
  data() {
    return {
    };
  },
  props: {
  },
  methods: {
  },

  created(){

  }
};
</script>

<style>
.post-list-cont {
  /* padding-top: 80px; */
  display: flex;
  flex-direction: column;
  text-align: left;
  font-size: 1rem;
  max-width: 547px; /* 1px~447px표시 아무리큰화면이라도 447px까지표시 모바일은 1까지줄어듬 */
  margin-left: auto;
  margin-right: auto;
}
@media (min-width: 577px) {
  /* 현재 넓이가 577px부터 탑 패딩추가 */
  .post-list-cont {
    padding-top: 10vh;
  }
}
.post-list-info {
  padding: 16px;
}
.post-list-search {
  margin-bottom: 2rem;
}
.post-list-search > h6 {
  margin-top: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #212529;
  overflow: hidden;
  white-space:nowrap;
  text-overflow: ellipsis;
}
#searcPost {
  height: 3rem;
}
.post-list {
  padding-bottom: 3rem;
}
.post-list-title:hover {
  text-decoration: none;
}
.post-list-title > h2 {
  font-size: 1.5rem;
  margin: 0px;
  color: #212529;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /** 글을 줄바꿈하지않음 */
  font-weight: bold;
}
.post-list-content {
  margin-bottom: 1rem;
  margin-top: 0.5rem;
  font-size: 1rem;
  color: #495057;
  text-align: left;
  overflow: hidden; /** 넘치는 글 숨김 */
  word-break: break-all; /** 글을 줄바꿈 */
  max-height: 75px; /** 글을 최대 3줄까지 표시함 */
}
.post-list-subinfo {
  display: flex;
  margin-top: 1rem;
  color: #868E96;
  font-size: 0.875rem;
}
.post-list-comment{
  padding-left: 10px;
}
</style>