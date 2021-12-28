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
// 파이어베이스 유저정보권한 초기화 후 렌더링 시작
// 1.router 내부에서 권한 체크를 위해선 파이어베이스 auth의 객체생성이 먼저 이루어져야한다
// 2.비동기적으로 처리되는 유저갱신(로그인/새로고침)을 감지하여 렌더링전에 권한갱신을 하기 위함 
// 3.재랜더링 될때마다 아래의 권한확인 후 할당부분이 실행된다. 
firebase.onAuthStateChanged(firebase.auth, async (user) => {
    // 갱신해온 정보에 유저정보가 있으면 JWT를 갱신하고 유저이메일, 정보를 저장한다
    if (user?.uid) {
        const ID_TOKEN=await user.getIdToken() // 토큰취득
        sessionStorage.setItem('jwt', ID_TOKEN); // 토큰을 세션에 저장 
        store.commit("onAuthEmailChanged", user.email); // 이메일 저장
        store.commit("onUserStatusChanged", true); // 로그인 상태 OK 저장
    } else {
        // 갱신해온 정보에 유저정보가 없다면 JWT와 기존유저정보를 지움
        sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
        store.commit("onAuthEmailChanged", ""); // 저장된 이메일 비움
        store.commit("onUserStatusChanged", false); // 로그인 상태 NG 저장
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