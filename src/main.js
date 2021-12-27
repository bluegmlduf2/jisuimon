import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import store from '@/store.js';
import router from '@/router.js';
import message from '@/assets/js/message'
import moment from "moment";
import firebase from '@/firebase'; // fireBas초기화

const app=createApp(App);

//파이어베이스 초기화
firebase.init();
firebase.onAuth(); // 인가처리 TODO 한번체크

// 전역변수
moment.locale("ja");// moment 일본어 적용;
app.config.globalProperties.$message=message; //message
app.config.globalProperties.$moment=moment;
// 플러그인
app.use(store); // vuex
app.use(router); // router
app.mount('#app')