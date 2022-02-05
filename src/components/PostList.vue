<template>
  <div class="post-list-cont">
    <div class="post-list-search">
      <h6>作成した投稿から食材で検索します</h6>
      <div class="post-list-search-input">
        <input
          class="form-control sm-4 mr-2"
          id="searchPost"
          type="text"
          ref="foodInput"
          style="ime-mode: disabled"
          placeholder="食材を入力してください"
          @keyup="getFood"
          @change="selectFood"
          list="foodDataList"
          :disabled="selectedFood.food_clicked"
        />
        <button
          class="btn btn-sm bg-transparent material-icons"
          type="button"
          @click="clearFood"
          v-if="selectedFood.food_clicked"
        >
          clear
        </button>
        <datalist id="foodDataList">
          <option v-for="(food, i) in foodList" :key="i">
            {{ food["food_name"] }}
          </option>
        </datalist>
      </div>
    </div>
    <div class="post-list" v-for="(e, i) in postList" :key="i">
      <router-link :to="`/post/${e.post_id}`" class="post-list-title">
        <h2>{{ removeHtml(e.title) }}</h2>
      </router-link>
      <p class="post-list-content">
        {{ removeHtml(e.content) }}
      </p>
      <div class="post-list-subinfo">
        <span class="post-list-date">{{
          $moment(e.create_date).format("YYYY年 MM月 DD日 dddd")
        }}</span>
        <span class="separator">·</span>
        <span class="post-list-comment"> {{ e.comment_cnt }}件のコメント</span>
      </div>
    </div>
    <div v-if="postList.length == 0">投稿がありません</div>
  </div>
  <div v-if="scrollSpinner" class="loader loader-black loader-1"></div>
</template>

<script>
import common from "@/assets/js/common.js";

export default {
  name: "PostList",
  mixins: [common],
  data() {
    return {
      postCnt: 5, //현재 게시물 수
      postCntAll: 0, // 총 게시물 수
      scrollSpinner: false, // 게시물 더보기 스피너
      postList: [], // 게시물리스트
      foodList: [], // 검색한 재료리스트
      selectedFood: {
        // 선택중인 재료
        food_id: null, //음식 ID
        food_name: null, //음식 이름
        food_clicked: false, // 음식이 선택된지 여부
      },
    };
  },
  methods: {
    // 게시물 리스트
    getPostList(postReload = false) {
      // 음식명으로 검색시 기존 데이터 초기화
      if (postReload) {
        this.postCnt = 5;
        this.postCntAll = 0;
        this.postList = []; // 초기화        
      }

      const payload = {
        method: "get",
        sendData: { postCnt: this.postCnt, ingredientId: "" },
      };

      // 음식명으로 검색시
      if (this.selectedFood.food_id) {
        payload.sendData.ingredientId = this.selectedFood.food_id;
      }

      // 요청대기 스피너 보기 (초기화면만)
      if (this.postCnt == 5) {
        this.$store.commit("showSpinner");
      }

      this.$store
        .dispatch("postList", payload)
        .then((result) => {
          this.postList.push(...result.data[0]); //게시물 리스트
          this.postCntAll = result.data[1]; // 총 게시물 수
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.scrollSpinner = false; // 게시물더보기 스피너 보지않기
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 재료 검색 결과리스트 가져오기
    getFood(event) {
      const INPUT_FOOD = event.target.value; // 입력한 재료
      // 2글자 이상부터 검색
      if (INPUT_FOOD.length < 2) {
        return;
      }
      const payload = {
        method: "get",
        sendData: { food_name: INPUT_FOOD },
      };
      this.$store
        .dispatch("food", payload)
        .then((result) => {
          this.foodList = result.data;
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        });
    },
    // 선택한 재료 추가
    selectFood(event) {
      const CLICKED_OPTION = event.target; // 선택한 재료

      // 선택한 재료의 정보 가져오기
      const SELECTED_FOOD = this.foodList.find(
        (e) => e.food_name === CLICKED_OPTION.value
      );

      // 음식목록에서 선택한것이 아닌 일반 입력은 막기
      if (!SELECTED_FOOD) {
        return;
      }

      SELECTED_FOOD.food_clicked = true; // 선택중인 재료 입력창 입력금지 처리

      // 선택중인 재료 임시로 넣기
      Object.assign(this.selectedFood, SELECTED_FOOD);

      // 음식명으로 검색
      this.getPostList(true);
    },
    // 선택중인 재료정보 삭제
    clearFood() {
      this.selectedFood.food_id = null;
      this.selectedFood.food_name = null;
      this.selectedFood.food_clicked = false;
      this.foodList = [];
      this.$refs.foodInput.value = null;
      // 음식명으로 검색
      this.getPostList(true);
    },
    // 무한스크롤 정의
    moveScroll(e) {
      const { scrollHeight, scrollTop, clientHeight } =
        e.target.documentElement;
      const scrollPos = Math.floor(scrollTop + clientHeight);
      // scrollHeight 화면바닥의px === scrollPos 스크롤위치
      const isAtTheBottom = scrollHeight === scrollPos;
      // 스크롤이 화면 최하단일 경우 추가게시물 호출 함수 실행
      if (isAtTheBottom) this.loadPages();
    },
    // 추가 게시물 가져오기
    loadPages() {
      // 내려오면 api 호출하여 아래에 더 추가, total값 최대이면 호출 안함
      if (this.postCnt < this.postCntAll) {
        this.postCnt = this.postCnt + 5;
        this.scrollSpinner = true; // 게시물더보기 스피너 보기
        this.getPostList();
      }
    },
  },
  // 화면초기화
  created() {
    this.getPostList(); // 게시물 리스트 초기화
  },
  // 스크롤 함수 이벤트 초기화
  mounted() {
    window.addEventListener("scroll", this.moveScroll);
  },
  // 스크롤 함수 이벤트 해제
  unmounted() {
    window.removeEventListener("scroll", this.moveScroll);
  },
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
  margin-bottom: 1.5rem;
}
.post-list-search > h6 {
  margin-top: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #212529;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.post-list-search-input {
  display: flex;
}
#searchPost {
  height: 3rem;
}
.post-list {
  height: 150px;
  padding: 1.2rem 0 1rem;
  border-top: 1px solid #f1f3f5;
}
.post-list-title:hover {
  text-decoration: none;
}
.post-list-title > h2 {
  font-size: 1.5rem;
  color: #212529;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /** 글을 줄바꿈하지않음 */
  font-weight: bold;
}
.post-list-content {
  margin: 0.5rem 0;
  font-size: 1rem;
  color: #495057;
  text-align: left;
  overflow: hidden; /** 넘치는 글 숨김 */
  word-break: break-all; /** 글을 줄바꿈 */
  max-height: 50px; /** 글을 최대 3줄까지 표시함 */
}
.post-list-subinfo {
  display: flex;
  /* margin-top: 1rem; */
  color: #868e96;
  font-size: 0.875rem;
}
.post-list-comment {
  padding-left: 10px;
}
</style>