import { createWebHistory, createRouter } from "vue-router";
import Post from "./components/Post.vue";
import PostList from "./components/PostList.vue";
import Card from "./components/Card.vue";
import Comment from "./components/Comment.vue";
import Write from "./components/Write.vue";
import Setting from "./components/Setting.vue";
import NotFound from "./components/NotFound.vue";
import firebase from "@/firebase";
import store from "@/store.js";
import message from "@/assets/js/message";

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
        path: "/postlist",
        components: {
            PostList: PostList,
        },
    },
    {
        path: "/write",
        components: {
            Write: Write,
        },
        meta: {
            requiresAuth: true,
        },
    },
    {
        path: "/setting",
        components: {
            Setting: Setting,
        },
        meta: {
            requiresAuth: true,
        },
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
    scrollBehavior() {
        // 새로고침 후 항상 최상단 표시
        return { top: 0 };
    },
});

//모든 라우터 들이 실행되기 전에 실행되는 녀석을 추가 (navigation guard)
router.beforeEach(function(to, from, next) {
    controlPagePartStatus(to) // 화면에따라 컴포넌트의 상태를 제어함
    movePageAfterAuthCheck(to, next); // 페이지권한 확인후 이동
});

// 화면에따라 컴포넌트의 상태를 제어함
function controlPagePartStatus(to) {
    // 게시물리스트 화면표시할때 nav의 음식검색 창을 표시하지않음 
    if (to.path=="/postlist") {
        store.commit("hideFoodSearchStatus"); // nav의 음식검색 창을 표시안함
    }else{
        store.commit("showFoodSearchStatus"); // nav의 음식검색 창을 표시
    }
}

// 페이지권한 확인후 이동
function movePageAfterAuthCheck(to, next) {
    firebase.onAuth(); // app의 권한갱신과는 다르게 페이지 이동시마다 권한갱신을한다
    let currentUserStatus = store.getters["isSignedIn"];
    let requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

    // 인증필요페이지 구분
    if (requiresAuth) {
        // 인증이 필요한 페이지

        // 로그인한 상태일 경우 화면이동
        if (currentUserStatus) {
            next();
        } else {
            // 로그인안한 상태일 경우 경고후 홈화면으로 이동
            message.infoMessage("TODO 로그인필요함").then(() => {
                const HOME_URL = `/${location.pathname.split("/")[1]}`;
                location.href = HOME_URL;
            });
        }
    } else {
        //인증이 필요없는 페이지
        next();
    }
}

export default router;
