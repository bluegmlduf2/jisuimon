import { createWebHistory, createRouter } from "vue-router";
// import Main from './components/Main.vue'
import Post from "./components/Post.vue";
import Card from "./components/Card.vue";
import Comment from "./components/Comment.vue";
import Write from "./components/Write.vue";
import NotFound from "./components/NotFound.vue";
import { getAuth , onAuthStateChanged} from "firebase/auth"; // fireBase인증관련
//$route : 경로관련
//$router : 페이지이동관련

const routes = [
    {
        path: "/",
        components: {
            Card: Card,
        }
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
        meta:{
            authRequired: true
        }
    },
    {
        path: "/:catchAll(.*)",
        components: {
            NotFound: NotFound,
        },
    },
];

//createRouter() vue-router는 원래 이 부분만 사용한다.
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    scrollBehavior(){
        // 새로고침 후 항상 최상단 표시
        return { top: 0 }
    }
});

//모든 라우터 들이 실행되기 전에 실행되는 녀석을 추가 (navigation guard)
router.beforeEach(function (to, from, next) {
    // 인증필요페이지 구분
    if (to.matched.some(record => record.meta.authRequired)) {
        //인증이 필요한 페이지
        const auth=getAuth() //현재 인증 상태 가져오기

        // 로그인한 상태일 경우 화면이동
        if (auth.currentUser) {
            next()
        }
        // 인증정보에 로그인정보가 있으면 이동
        onAuthStateChanged(auth, (user) => {
            if (user) {
                next()
            } else {
                next({path:"/"})
                alert('로그인하셈')
            }
        });
    }else{
        //인증이 필요없는 페이지
        next()
    }
    
    // next() // 인증정보가 필요없는 화면일 경우 그냥 이동
});

export default router;
