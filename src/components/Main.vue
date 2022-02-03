<template>
  <div class="container-fluid">
    <!-- Main -->
    <router-view name="Card" :posts="posts" :postCnt="postCnt" :postCntAll="postCntAll" @addPostCnt="addPostCnt"/>
    <!-- Post -->
    <router-view name="Post" />
    <!-- PostList -->
    <router-view name="PostList" />
    <!-- Setting -->
    <router-view name="Setting" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <!-- Write -->
    <router-view name="Write" v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <!-- Error -->
    <router-view name="NotFound" />
    <!-- 요청대기용 스피너 -->
    <div class="loader-background" v-if="getSpinner">
      <div class="regot-loader">
        <div class="regot regot1"></div>
        <div class="regot regot2"></div>
        <div class="regot regot3"></div>
        <div class="regot regot4"></div>
      </div>
    </div>
    <!-- 게시물더보기용 스피너 -->
    <div v-if="scrollSpinner" class="loader loader-black loader-1"></div>
  </div>
</template>

<script>
export default {
  name: "Main",
  data() {
    return {
      posts: [],
      postCnt: 8, //현재 게시물 수
      postCntAll: 0, // 총 게시물 수
      scrollSpinner: false, // 게시물 더보기 스피너
    };
  },
  computed: {
    // 요청대기 스피너 초기값반환
    getSpinner() {
      return this.$store.getters["getSpinner"];
    },
  },
  methods: {
    // 메인게시물 호출
    getPosts() {
      const payload = {
        method: "get",
        sendData: { postCnt: this.postCnt },
      };

      // 요청대기 스피너 보기 (초기화면만)
      if (this.postCnt == 8) {
        this.$store.commit("showSpinner");
      }

      this.$store
        .dispatch("post", payload)
        .then((result) => {
          this.posts.push(...result.data);
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.scrollSpinner = false; // 게시물더보기 스피너 보지않기
          this.$store.commit("hideSpinner"); // 요청대기 스피너 보지않기
        });
    },
    // 총 게시물수 가져오기
    getPostCount() {
      const payload = {
        method: "get",
      };
      this.$store
        .dispatch("getPostCount", payload)
        .then((result) => {
          this.postCntAll = result.data.postCntAll;
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        });
    },
    // 게시물 8개 더 보여주기
    addPostCnt() {
      this.postCnt = this.postCnt + 8;
      this.scrollSpinner = true; // 게시물더보기 스피너 보기
      this.getPosts();
    },
  },
  created() {
    const IS_HOME_ROUTER = this.$route.path == "/"; // 현재 화면의 라우터가 홈라우터인지 여부
    const IS_MAIN_PATH = !location.pathname.split("/")[2]; // 현재 화면이 홈화면인지 여부
    if (IS_HOME_ROUTER && IS_MAIN_PATH) {
      this.getPosts();
      this.getPostCount();
    }
  },
};
</script>

<style>
/* 메인 레이아웃 css (부트스트랩 스마트폰 가로 기준(576px미만) 으로 작성)*/
@media (max-width: 576.98px) {
  .container-fluid {
    padding-top: 80px;
  }
}

/* transition의 페이지 이동시 fade 애니메이션
transition태그의 name=fade를 참고함. enter-active는 뷰에서제공*/
.fade-enter-active {
  transition: opacity 1s ease;
}

.fade-enter-from {
  opacity: 0;
}

/* 요소에 포커스가 발생시 기존 부트스트랩 애니메이션 제거 (a태그이외) */
*:focus:not(a) {
  outline: none !important;
  border-color: rgb(206, 212, 218) !important;
  box-shadow: rgb(0 0 0 / 20%) 0px 0px 10px !important;
}

/*-------------------------------------------
    $ Loaders 스피너 (요청대기용)
-------------------------------------------*/
.loader-background {
  background-color: rgba(249, 249, 249, 0.85);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0; /* 모달배경을 꽉차게설정 top~bottom 0 설정이유 */
  width: 100%;
  z-index: 9999;
  display: flex; /* 아래는 플렉스를 이용한 가운데 정렬 */
  justify-content: center;
  align-items: center;
}
.regot-loader {
  font-size: 20px;
  position: fixed;
  transform: translateX(-50%); /** fixed의 width를 고려한 정중앙위치 */
  width: 4em;
  height: 1em;
  /* margin: 100px auto; */
  top: 50%;
  left: 50%;
}

.regot {
  width: 1em;
  height: 1em;
  border-radius: 0.5em;
  background: rgb(134, 142, 150);
  position: absolute;
  animation-duration: 0.5s;
  animation-timing-function: ease;
  animation-iteration-count: infinite;
}

.regot1,
.regot2 {
  left: 0;
}

.regot3 {
  left: 1.5em;
}

.regot4 {
  left: 3em;
}

@keyframes show {
  from {
    transform: scale(0.001);
  }
  to {
    transform: scale(1);
  }
}

@keyframes remove {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(0.001);
  }
}

@keyframes shift {
  to {
    transform: translateX(1.5em);
  }
}

.regot1 {
  animation-name: show;
}

.regot2,
.regot3 {
  animation-name: shift;
}

.regot4 {
  animation-name: remove;
}

/*-------------------------------------------
    $ Loaders 스피너 (게시물더보기용)
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

.loader-black {
  background-color: #333;
}

.loader-1 {
  animation-name: loader1;
}
@keyframes loader1 {
  from {
    transform: scale(0);
    opacity: 1;
  }
  to {
    transform: scale(1);
    opacity: 0;
  }
}
</style>