<template>
  <div class="container-fluid">
    <!-- Main -->
    <router-view name="Card" :posts="posts" />
    <!-- Post -->
    <router-view name="Post" :posts="posts" />
    <!-- Write -->
    <router-view name="Write" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <!-- Error -->
    <router-view name="NotFound" />
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
      posts: [],
    };
  },
  methods: {
    // 메인게시물 호출
    getPosts() {  
      this.loading = true;
      const payload = {method: "post"};
      this.$store.dispatch('post',payload).then((result) => {
        this.posts=result.data
      }).catch((err) => {
        this.$message.errorMessage(err);
      }).finally(()=>{
        this.loading = false;
      });
    },
  },
  created(){
    this.getPosts()
  }
};
</script>

<style>
/* 메인 레이아웃 css */
@media (max-width: 576.98px) {
  .container-fluid {
    padding-top: 80px;
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