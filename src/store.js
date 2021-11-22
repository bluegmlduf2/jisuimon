import { createStore } from "vuex";
import axios from "axios";

const rootUrl = process.env.VUE_APP_SERVER_URL; //

const store = createStore({
    // 해당영역(sotre.js)에서 vue의 전역변수사용 불가.
    // 데이터 저장하는곳 , $store.state
    state() {
        return {
            like: 0,
            selectedLike: false,
            moreDataVuex: null,
        };
    },
    // 데이터 변경하는곳 (디버깅등을 염두해서 데이터 변경을 한곳에서 처리) , $store.commoit()
    mutations: {
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
    actions: {
        // 메인 게시물 리스트 가져오기
        post(context, payload) {
            return axios({
                url: `${rootUrl}/post`,
                method: payload.method,
                params: payload,
                data: payload,
            });
        },
        // 게시물 상세정보 가져오기
        postDetail(context, payload) {
            return axios({
                url: `${rootUrl}/postDetail`,
                method: payload.method,
                params: payload,
                data: payload,
            });
        },
    },
});

export default store;
