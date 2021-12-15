<template>
    <!-- 아래의 <div class="card-deck".. 에서 v-for을 사용하면 vue의 태그로써 사용되기때문에 그 위에 root div를 사용해야한다. 아니면 경고남. -->
    <div>
        <!-- 게시물의 행 ~ 2 -->
        <div class="card-deck" v-for="i in Math.ceil(parseFloat(posts.length/4))" :key="i">
            <!-- 게시물의 열 ~ 4 -->
            <div class="card" v-for="x in 4" :key="x" :class="{'card-hidden': !getPostObj(posts,i,x) }">
                <div v-if="getPostObj(posts,i,x)">
                    <router-link :to="`/post/${getPostObj(posts,i,x).post_id}`">
                        <!-- <img :src="require(`/${getPostObj(posts,i,x).title_image}`)" class="card-img-top" alt=""> -->
                        <img :src="`${getPostObj(posts,i,x).title_image}`" class="card-img-top" alt="">
                        <div class="card-body">
                            <h5 class="card-title">{{removeHtml(getPostObj(posts,i,x).title)}}</h5>
                            <p class="card-text card-content" v-text="removeHtml(getPostObj(posts,i,x).content)"/>
                            <p class="card-text card-date"><small class="text-muted">{{$moment(getPostObj(posts,i,x).create_date).fromNow()}}</small></p>
                        </div>
                        <div class="card-bottom">
                            <div class="card-writer">
                                <img :src="`${getPostObj(posts,i,x).user_image}`" alt="postWriterImg">
                                <small>by {{getPostObj(posts,i,x).nickname}}</small>
                            </div>
                            <div class="card-like">
                                <span class="material-icons">favorite</span>{{getPostObj(posts,i,x).like_cnt}}
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import common from "@/assets/js/common.js";

export default {
  name: "Card",
  mixins: [common],
  data() {
    return {
      cardDeckCnt: 3,
      cardCnt: 11,
    };
  },
  props: {
    posts: Array,
  },
  methods: {
    // 게시물의 행과 열에 맞는 데이터를 반환한다
    getPostObj(post, i, x) {
      return post[(i - 1) * 4 + x - 1];
    },
    // 무한스크롤 정의
    moveScroll(e) {
        const { scrollHeight, scrollTop, clientHeight } = e.target.documentElement;
      const isAtTheBottom = scrollHeight === scrollTop + clientHeight;
      // 일정 한도 밑으로 내려오면 함수 실행
      if (isAtTheBottom) this.loadPages();
    },
    // 내려오면 api 호출하여 아래에 더 추가, total값 최대이면 호출 안함
    loadPages() {
    //TODO 둥근프로그레스바 구현
    console.log(1)
    
    //   if (this.notifications.length < this.total) {
    //     const params = {
    //       limit: this.params.limit,
    //       page: this.params.page + 1
    //     };
    //     this.$store.commit(
    //       "notification/SET_PARAMS",
    //       this.filterValue ? { ...params, type: this.filterValue } : params
    //     );
    //     this.dispatchGetNotifications(false);
    //   }
    },
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

.card-deck{
  border-radius: 4px;
}
@media (min-width: 576px){
  .card-deck{
    padding-top: 80px;
  }
}
.card{
  border: 0 !important;;
  outline: 0;
}
.card {
  transition: transform 250ms;
}
.card:hover {
  transform: translateY(-10px);
  /* offset-x | offset-y | blur-radius | spread-radius | color */
  box-shadow: 45px 45px 40px -30px rgb(240, 240, 245);
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
.card a{
    /* anchor 태그 초기화 (Bootstrap때문에 important사용)*/
    color: inherit !important; /* 상위에서 사용한 fontcolor사용 */
    text-decoration: inherit !important; /* no underline */
}
.card-img-top{
    height: 230px;
}
.card-body{
    height: 205px;
    position: relative;
}
.card-title{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.card-content{
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 100px;
}
.card-date{
    position: absolute;
    bottom:10px
}
.card-hidden{
    visibility: hidden;
}
.card-bottom{
  display: flex;
  justify-content: space-between; /** 요소가 일정한 간격을 두고 떨어짐, 2개 요소가 좌우로 최대한 멀어짐 */
  padding: 0.5rem;
  border-top: 1px solid rgb(248, 249, 250);
}
.card-writer{
    display: flex;
}
.card-writer > img {
  height: 1.5rem;
  widows: 1.5rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
  margin:0 0.5rem;
}
.card-like > span{
    position: relative;
    top: 2px;
    font-size: 1rem;
    padding-right: 0.5rem;
}
</style>