import { createWebHistory, createRouter } from "vue-router";
// import Main from './components/Main.vue'
import Post from "./components/Post.vue";
import Card from "./components/Card.vue";
import Comment from "./components/Comment.vue";
import Write from "./components/Write.vue";
import NotFound from "./components/NotFound.vue";
//$route : 경로관련
//$router : 페이지이동관련

const routes = [
    {
        path: "/",
        components: {
            Card: Card,
        },
    },
    {
        path: "/post/:postId",
        components: {
            Post: Post,
            Comment: Comment,
        },
        props: true,
    },
    {
        path: "/write",
        components: {
            Write: Write,
        },
    },
    {
        path: "/NotFound",
        components: {
            NotFound: NotFound,
        },
    },
];

//createRouter() vue-router는 원래 이 부분만 사용한다.
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

//모든 라우터 들이 실행되기 전에 실행되는 녀석을 추가 (navigation guard)
router.beforeEach((to, from, next) => {

  console.log(to)
  console.log(from)
  console.log(next())
    // if (!isNaN(to.params.id)) {
    //     next();
    // } else {
    //     next(false); //or show message error (maybe redirect to a /error)
    // }
});

export default router;
