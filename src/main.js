import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import store from './store.js';
import router from './router.js';
import message from './assets/js/message'
import moment from "moment";
import { initializeApp } from "firebase/app"; // fireBase초기화관련(SDK v9)
import firebaseConfig from '@/firebase'; // fireBas설정파일
import { getAuth } from "firebase/auth"; // fireBase인증관련

const app=createApp(App);

// 전역변수
moment.locale("ja");// moment 일본어 적용
app.config.globalProperties.$message=message; //message
app.config.globalProperties.$moment=moment;
// 플러그인
initializeApp(firebaseConfig) // fireBase 초기화
app.config.globalProperties.$auth=getAuth(); // fireBase인증
app.use(store); // vuex
app.use(router); // router
app.mount('#app')