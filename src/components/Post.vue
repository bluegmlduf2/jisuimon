<template>
  <div class="postCont">
    <h1 class="postCont_title">{{ posts.title }}</h1>
    <div class="postCont_writer">
      <b>{{ posts.nickname }}</b
      >&nbsp;&nbsp;&nbsp;{{
        $moment(posts.create_date).format("YYYY年 MM月 DD日 dddd")
      }}
    </div>
    <div class="postCont_ingredient">
      <span v-for="i in ingredient" :key="i.ingredient_id">{{
        i.ingredient_name
      }}</span>
    </div>
    <div class="postCont_index">
      <h3>김치찌게만들기 목록</h3>
      <ol v-if="listShow">
        <li>순서1</li>
        <li>순서2</li>
        <li>순서3</li>
        <li>순서4</li>
        <li>순서5</li>
      </ol>
      <div class="postCont_index_list" @click="listShow = !listShow">
        {{ listShow ? "▲ 숨기기" : "▼ 목록보기" }}
      </div>
    </div>
    <div class="postCont_article">
      <p v-html="posts.content"></p>
    </div>
    <div>
      <Comment :comment="comment" />
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
  setup(){

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
      this.loading = true;
      const payload = {method: "get", postId: this.$route.params.postId};
      this.$store
        .dispatch("postDetail", payload)
        .then((result) => {
          console.log(result)
          this.posts = result.data[0]; //게시물 상세정보
          this.comment = result.data[1]; //게시물 댓글정보
          this.ingredient = result.data[2]; //게시물 재료정보
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.loading = false;
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
  .postCont{
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
  margin-bottom: 20px;
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
  height: 1.5rem;
  font-size: 1rem;
  border-radius: 0.75rem;
  padding: 1rem;
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
  margin-top: 2.5rem;
  cursor: pointer;
}
.postCont_article {
  line-height: 1.75; /* 폰트사이즈16px*1.75 */
  padding-bottom: 70px;
}
@media (min-width: 577px) {
  /* 현재 넓이가 577px이상 */
  .postCont {
    padding-top: 10vh;
  }
}
</style>