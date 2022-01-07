import { createStore } from "vuex";
import axios from "axios";

const rootUrl = process.env.VUE_APP_SERVER_URL; // env파일에 저장된 서버 Root_url
// Axios의 기본 객체 생성
const instance = axios.create({
    baseURL: rootUrl,
    // timeout: 3000,
});
// axios 인터셉터 인증정보처리
instance.interceptors.request.use(
    (config) => {
        let token = sessionStorage.getItem("jwt");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        Promise.reject(error);
    }
);

const store = createStore({
    // 해당영역(sotre.js)에서 vue의 전역변수사용 불가.
    // 데이터 저장하는곳 , $store.state
    state() {
        return {
            email: "", // 유저 이메일 정보
            status: false, // 유저 로그인 상태
            like: 0,
            selectedLike: false,
            moreDataVuex: null,
            getRequest: (url, payload, fileUpload = false) => {
                // Axios의 기본 정보
                const option = {
                    url: url,
                    method: payload.method,
                };

                // 파일업로드인 경우 헤더의 타입을 변경
                if (fileUpload) {
                    option.headers["content-Type"] = "multipart/form-data";
                }

                // Axios의 메서드에 따라서 파라메터 타입을 지정해줌
                const dataType =
                    payload.method == "get"
                        ? { params: payload.sendData }
                        : { data: payload.sendData };

                // Axios의 기본객체반환
                return instance(Object.assign(option, dataType));
            },
        };
    },
    getters: {
        // 유저이메일정보
        email(state) {
            return state.email;
        },
        // 로그인상태
        isSignedIn(state) {
            return state.status;
        },
    },
    // 데이터 변경하는곳 (디버깅등을 염두해서 데이터 변경을 한곳에서 처리) , $store.commoit()
    mutations: {
        // 유저 이메일 정보 갱신
        onAuthEmailChanged(state, email) {
            state.email = email;
        },
        // 유저 로그인 상태 갱신
        onUserStatusChanged(state, status) {
            state.status = status;
        },
        addLike(state) {
            state.like++;
            state.selectedLike = true;
        },
        removeLike(state) {
            state.like--;
            state.selectedLike = false;
        },
        //vuex action 테스트용, 두번째 인자는 전달받는값
        showMoreVuex(state, data) {
            state.moreDataVuex = data;
            console.log(state.moreDataVuex);
        },
    },
    // Ajax데이터 요청등을 처리 , $store.dispatch()
    // 하나의 메서드로 안쓰고 메서드를 분리한 이유는 인터페이스 개념으로 url들을 파악하기 위해서
    actions: {
        // 메인 게시물 리스트 가져오기 , 게시물 등록
        post(context, payload) {
            return this.state.getRequest("/post", payload);
        },
        // 총 게시물 수 가져오기
        getPostCount(context, payload) {
            return this.state.getRequest("/postcount", payload);
        },
        // 게시물 상세정보 가져오기
        postDetail(context, payload) {
            return this.state.getRequest("/postDetail", payload);
        },
        // 음식리스트가져오기
        food(context, payload) {
            return this.state.getRequest("/food", payload);
        },
        // 댓글 등록
        comment(context, payload) {
            return this.state.getRequest("/comment", payload);
        },
        // 대댓글 등록
        commentReply(context, payload) {
            return this.state.getRequest("/commentReply", payload);
        },
        // 회원등록
        signUp(context, payload) {
            return this.state.getRequest("/user", payload);
        },
        // 회원삭제
        deleteUser(context, payload) {
            return this.state.getRequest("/user", payload);
        },
        // 회원이미지등록
        userImage(context, payload, fileUpload = false) {
            return this.state.getRequest("/userImage", payload, fileUpload);
        },
    },
});

export default store;
