<template>
  <div class="container-fluid">
    <!-- Main -->
    <router-view name="Card" :posts="posts" :postCnt="postCnt" :postCntAll="postCntAll" @addPostCnt="addPostCnt"/>
    <!-- Login -->
    <router-view name="Login" />
    <!-- Post -->
    <router-view name="Post" />
    <!-- Write -->
    <router-view name="Write" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <!-- Error -->
    <router-view name="NotFound" />
    <div v-if="showSpinner" class="loader loader-black loader-1"></div>
  </div>
</template>

<script>
export default {
  name: "Main",
  components: {
    // Card:Card
  },
  data() {
    return {
      loading: false,
      posts: [],
      postCnt: 8, //현재 게시물 수
      postCntAll: 0, // 총 게시물 수
      showSpinner:false
    };
  },
  methods: {
    // 메인게시물 호출
    getPosts() {  
      const payload = {
        method: "get",
        sendData: { postCnt: this.postCnt },
      };
      this.$store.dispatch('post',payload).then((result) => {
        this.posts.push(...result.data)
      }).catch((err) => {
        this.$message.errorMessage(err);
      }).finally(()=>{
        this.showSpinner = false
      });
    },
    // 총 게시물수 가져오기
    getPostCount(){
      const payload = {
        method: "get"
      };
      this.$store.dispatch('getPostCount',payload).then((result) => {
        this.postCntAll=result.data.postCntAll
      }).catch((err) => {
        this.$message.errorMessage(err);
      })
    },
    // 게시물 8개 더 보여주기
    addPostCnt(){
      this.showSpinner = true

      setTimeout(() => {
        this.postCnt=this.postCnt+8
        this.getPosts()                  
      }, 2000);
    }
  },
  created(){
    this.getPosts()
    this.getPostCount()
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

/*-------------------------------------------
    $ Loaders 스피너
-------------------------------------------*/
.loader {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin: 3em;
    display: inline-block;
    position: relative;
    vertical-align: middle;
}
.loader,
.loader:before,
.loader:after {
    animation: 1s infinite ease-in-out;
}
.loader:before,
.loader:after {
    width: 100%; 
    height: 100%;
    border-radius: 50%;
    position: absolute;
    top: 0;
    left: 0;
}

.loader-black { background-color: #333; }

.loader-1 { animation-name: loader1; }
@keyframes loader1 {
    from { transform: scale(0); opacity: 1; }
    to   { transform: scale(1); opacity: 0; }
}

</style>