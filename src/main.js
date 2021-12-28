import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import store from '@/store.js';
import router from '@/router.js';
import message from '@/assets/js/message'
import moment from "moment";
import firebase from '@/firebase'; // 파이어베이스 관련파일

//뷰객체
let app

// 파이어베이스 초기화
firebase.init();
// 파이어베이스 유저정보권한 초기화후 렌더링 시작 (비동기 유저갱신시 권한갱신)
// 1.비동기적으로 처리되는 유저갱신(로그인등..)을 감지하여 렌더링전에 권한갱신을 하기 위함 
// 2.예를들어 로그인시 state를 commit으로 갱신해준다. 이것이 감지되고 app이 재랜더링 되면서 아래의 권한갱신이 실행된다. 
firebase.onAuthStateChanged(firebase.auth, async (user) => {
    // 갱신해온 정보에 유저정보가 있으면 JWT를 갱신하고 유저이메일, 정보를 저장한다
    if (user) {
        // 토큰을 세션에 설정
        await user.getIdToken().then((idToken) => {
            sessionStorage.setItem('jwt', idToken);
        })
        .catch(() => {
            sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
        });

        store.commit("onAuthEmailChanged", user.email); // 이메일 저장
        if (user.uid) {
            store.commit("onUserStatusChanged", true); // 로그인 OK
        } else {
            store.commit("onUserStatusChanged", false); // 로그인 NG
        }
    } else {
        // 갱신해온 정보에 유저정보가 없다면 JWT와 기존유저정보를 지움
        store.commit("onAuthEmailChanged", "");
        store.commit("onUserStatusChanged", false);
    }

    // vue의 app객체를 최초 1회만 생성
    if(!app){
        // 뷰객체생성
        app = createApp(App);
        // 전역변수
        moment.locale("ja");// moment 일본어 적용;
        app.config.globalProperties.$message=message; //message
        app.config.globalProperties.$moment=moment;
        // 플러그인
        app.use(store); // vuex
        app.use(router); // router
        app.mount('#app')        
    }
});