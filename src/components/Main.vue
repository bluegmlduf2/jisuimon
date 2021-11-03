<template>
  <div class="container-fluid">
    <!-- Main -->
    <router-view class="card" name="Card" :posts="posts" />
    <!-- Post -->
    <router-view class="post" name="Post" :posts="posts" />
    <router-view class="comment" name="Comment" />
    <!-- Write -->
    <router-view class="write" name="Write" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
// import Card from './Card.vue'
// import postDatas from "@/assets/js/posts.js";

export default {
  name: "Main",
  components: {
    // Card:Card
  },
  data() {
    return {
      loading: false,
      posts: this.getPosts(),
    };
  },
  methods: {
    // 메인게시물 호출
    async getPosts() {  
      this.loading = true;
      this.posts = await this.$store.dispatch('getPosts').then((result) => {
        return result.data;
      }).catch((err) => {
        this.message.errorMessage(err);
      }).finally(()=>{
        this.loading = false;
      });
    },
  },
};
</script>

<style>
/* 메인 레이아웃 css */
@media (max-width: 576.98px) {
  .container-fluid {
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
.card {
  transition: transform 250ms;
}
.card:hover {
  transform: translateY(-10px);
  /* offset-x | offset-y | blur-radius | spread-radius | color */
  box-shadow: 45px 45px 40px -30px rgb(240, 240, 245);
}

/* Post,Comment 공통 레이아웃 */
@media (min-width: 992px) {
  /* 넓이가 992px 이상 여백추가*/
  .postCont,
  .commentCont {
    text-align: left;
    padding-left: 160px;
    padding-right: 160px;
  }
}

/* transition의 페이지 이동시 fade 애니메이션
transition태그의 name=fade를 참고함. enter-active는 뷰에서제공*/
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 요소에 포커스가 발생시 기존 부트스트랩 애니메이션 제거 (a태그이외) */
*:focus:not(a) {
  outline: none !important;
  border-color: rgb(206, 212, 218) !important;
  box-shadow: rgb(0 0 0 / 20%) 0px 0px 10px !important;
}
</style>