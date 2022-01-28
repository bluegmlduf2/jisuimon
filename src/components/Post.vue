<template>
  <div class="postCont">
    <h1 class="postCont_title">{{ posts.title }}</h1>
    <div class="postCont_writer">
      <div class="postCont_writer_profile">
        <b>{{ posts.nickname }}</b>
        <span>{{$moment(posts.create_date).format("YYYY年 MM月 DD日 dddd")}}</span>
      </div>
      <div class="postCont_writer_button" v-if="posts.post_auth">
        <span>修正</span>
        <span>削除</span>
      </div>
    </div>
    <div class="postCont_ingredient">
      <span v-for="i in ingredient" :key="i.ingredient_id">
      {{`${i.ingredient_name}&emsp;/&nbsp;${i.ingredient_amt}${i.ingredient_unit}`}}
      </span>
    </div>
    <div class="postCont_index">
      <h3>材料詳細</h3>
      <ul v-if="listShow">
        <li v-for="i in ingredient" :key="i.ingredient_id">
          {{`${i.ingredient_name}&emsp;/&nbsp;${i.ingredient_amt}${i.ingredient_unit}`}}
        </li>
      </ul>
      <div class="postCont_index_list" @click="listShow = !listShow">
        {{ listShow ? "▲ 閉じる" : "▼ 開く" }}
      </div>
    </div>
    <div class="postCont_article">
      <p v-html="posts.content"></p>
    </div>
    <div>
      <!-- @updateCommentProps : emit을 이용해서 자식(comment)이 부모(post)의 data를 초기화(렌더링없음) -->
      <Comment :postId="posts.post_id" :comment="comment" @updateCommentProps="getPostDetail" />
    </div>
  </div>
</template>

<script>
import Comment from "./Comment.vue";

export default {
  name: "Post",
  components: {
    Comment: Comment,
  },
  data() {
    return {
      loading: false,
      listShow: false,
      posts: {},
      comment: {},
      ingredient: null,
    };
  },
  methods: {
    // 선택 게시물 상세내용
    getPostDetail() {
      const payload = {
        method: "get",
        sendData: { postId: this.$route.params.postId },
      };
      
      this.$store.commit('showSpinner'); // 요청대기스피너 보기
      
      this.$store
        .dispatch("postDetail", payload)
        .then((result) => {
          this.posts = result.data[0]; //게시물 상세정보
          this.comment = result.data[1]; //게시물 댓글정보
          this.ingredient = result.data[2]; //게시물 재료정보
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit('hideSpinner'); // 요청대기스피너 보지않기
        });
    },
  },
  created() {
    this.getPostDetail();
  },
};
</script>

<style>
.postCont {
  text-align: left;
}
@media (min-width: 577px) {
  /* 현재 넓이가 577px이상 */
  .postCont {
    padding-top: 10vh;
  }
}
/* Post,Comment 공통 레이아웃 */
@media (min-width: 992px) {
  /* 넓이가 992px 이상 여백추가*/
  .postCont {
    padding-left: 160px;
    padding-right: 160px;
  }
}

.postCont_title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 30px;
}
.postCont_writer {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.postCont_writer_profile span{
  margin-left: 0.5rem;
}
.postCont_writer_button{
  padding: 0px;
  outline: none;
  border: none;
  background: none;
  font-size: inherit;
  cursor: pointer;
  color: rgb(134, 142, 150);
  font-size: 0.9rem;
}
.postCont_writer_button > span{
  margin-left: 0.5rem;
}
.postCont_ingredient {
  margin-bottom: 20px;
}
.postCont_ingredient span {
  background: rgb(241, 243, 245);
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  color: rgb(12, 166, 120);
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  border-radius: 0.75rem;
  padding: 0.25rem 1rem;
  margin-right: 0.5rem;
  margin-bottom: 0.2rem;
}

.postCont_index {
  padding: 1rem;
  margin-top: 2rem 0;
  background: rgb(242, 242, 242);
  border-radius: 8px;
  box-shadow: rgb(0 0 0 / 6%) 0px 0px 4px 0px;
  position: relative;
  color: rgb(33, 37, 41);
  margin-bottom: 20px;
}
.postCont_index h3 {
  margin-bottom: 20px;
}
.postCont_index ol {
  font-size: 0.875rem;
  margin-bottom: -1rem;
  padding-left: 1.7rem;
}
.postCont_index ol li {
  margin-bottom: 0.5rem;
}
.postCont_index_list {
  cursor: pointer;
}
.postCont_article {
  line-height: 1.75; /* 폰트사이즈16px*1.75 */
  padding-bottom: 70px;
  word-break:break-all; /* 가로 넓이 벗어나면 줄바꿈 */
}

@media (min-width: 577px) {
  /* 현재 넓이가 577px이상 */
  .postCont {
    padding-top: 10vh;
  }

}

/* 메인 레이아웃 css (부트스트랩 스마트폰 가로 기준(576px미만) 으로 작성)*/
@media (max-width: 576.98px) {
  .postCont_article img {
    width: 100%;
  }
}
</style>