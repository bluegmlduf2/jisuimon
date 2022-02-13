<template>
  <div class="post-search-cont">
    <div class="post-search-search">
      <h6>食材で検索します</h6>
      <div class="post-search-search-input">
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
    <div class="post-search" v-for="(e, i) in postSearch" :key="i">
      <router-link :to="`/post/${e.post_id}`" class="post-search-title">
        <h2>{{ removeHtml(e.title) }}</h2>
      </router-link>
      <p class="post-search-content">
        {{ removeHtml(e.content) }}
      </p>
      <div class="post-search-subinfo">
        <span class="post-search-date">{{
          $moment(e.create_date).format("YYYY年 MM月 DD日 dddd")
        }}</span>
        <span class="separator">·</span>
        <span class="post-search-comment">
          {{ e.comment_cnt }}件のコメント</span
        >
      </div>
    </div>
    <div v-if="postSearch.length == 0">投稿がありません</div>
  </div>
  <div v-if="scrollSpinner" class="loader loader-black loader-1"></div>
</template>

<script>
import common from "@/assets/js/common.js";

export default {
  name: "PostSearch",
  mixins: [common],
  data() {
    return {
      postCnt: 5, //현재 게시물 수
      postCntAll: 0, // 총 게시물 수
      scrollSpinner: false, // 게시물 더보기 스피너
      postSearch: [], // 게시물리스트
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
    getPostSearch(clickedStatus) {
      const INGREDIENT_ID = this.$route.query?.ingredientId;

      // 음식명으로 검색시 & 클리어 버튼 클릭시 기존 데이터 초기화
      if (clickedStatus) {
        this.postCnt = 5;
        this.postCntAll = 0;
        this.postSearch = []; // 초기화
      }

      // 클리어버튼 클릭시 검색을 더이상 진행하지않음
      if (clickedStatus == "clear") {
        return
      }

      const payload = {
        method: "get",
        sendData: { postCnt: this.postCnt, ingredientId: "" },
      };

      // 음식명으로 검색시
      if (this.selectedFood.food_id) {
        payload.sendData.ingredientId = this.selectedFood.food_id;
      } else if (INGREDIENT_ID) {
        // 쿼리 파라미터로 검색시
        payload.sendData.ingredientId = INGREDIENT_ID;
      } else {
        // 검색조건이 존재하지 않기때문에 에러페이지로 이동
        this.$router.push("/error");
      }

      // 요청대기 스피너 보기 (초기화면만)
      if (this.postCnt == 5) {
        this.$store.commit("showSpinner");
      }

      this.$store
        .dispatch("postSearch", payload)
        .then((result) => {
          this.postSearch.push(...result.data[0]); //게시물 리스트
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
      // 2글자부터 30글자까지 검색
      if (INPUT_FOOD.length < 2 || INPUT_FOOD.length > 31) {
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
      this.getPostSearch('select');
    },
    // 선택중인 재료정보 삭제
    clearFood() {
      this.selectedFood.food_id = null;
      this.selectedFood.food_name = null;
      this.selectedFood.food_clicked = false;
      this.foodList = [];
      this.$refs.foodInput.value = null;
      // 음식명으로 검색
      this.getPostSearch('clear');
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
        this.getPostSearch();
      }
    },
  },
  // 화면초기화
  created() {
    this.getPostSearch(); // 게시물 리스트 초기화
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
.post-search-cont {
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
  .post-search-cont {
    padding-top: 10vh;
  }
}
.post-search-info {
  padding: 16px;
}
.post-search-search {
  margin-bottom: 1.5rem;
}
.post-search-search > h6 {
  margin-top: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #212529;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.post-search-search-input {
  display: flex;
}
#searchPost {
  height: 3rem;
}
.post-search {
  height: 150px;
  padding: 1.2rem 0 1rem;
  border-top: 1px solid #f1f3f5;
}
.post-search-title:hover {
  text-decoration: none;
}
.post-search-title > h2 {
  font-size: 1.5rem;
  color: #212529;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /** 글을 줄바꿈하지않음 */
  font-weight: bold;
}
.post-search-content {
  margin: 0.5rem 0;
  font-size: 1rem;
  color: #495057;
  text-align: left;
  overflow: hidden; /** 넘치는 글 숨김 */
  word-break: break-all; /** 글을 줄바꿈 */
  max-height: 50px; /** 글을 최대 3줄까지 표시함 */
}
.post-search-subinfo {
  display: flex;
  /* margin-top: 1rem; */
  color: #868e96;
  font-size: 0.875rem;
}
.post-search-comment {
  padding-left: 10px;
}
</style>