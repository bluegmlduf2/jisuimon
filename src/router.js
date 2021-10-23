import { createWebHistory, createRouter } from "vue-router";
// import Main from './components/Main.vue'
import Post from './components/Post.vue'
import Card from './components/Card.vue'
import Comment from './components/Comment.vue'
import Write from './components/Write.vue'
//$route : 경로관련
//$router : 페이지이동관련

const routes = [
  {
    path: '/',
    components: {
      Card:Card
    }
  },
  {
    path: '/post/:postId',
    components: {
      Post:Post,
      Comment:Comment
    },
    props:true
  },
  {
    path: "/write",
    components: {
      Write:Write
    }
  },
];

//createRouter() vue-router는 원래 이 부분만 사용한다.
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

//모든 라우터 들이 실행되기 전에 실행되는 녀석을 추가 (navigation guard)
router.beforeEach(() => {
    console.log('ip:'+"127.0.0.1")
})

export default router; 