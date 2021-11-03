import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
// import axios from 'axios'
import store from './store.js';
import router from './router.js';
import message from './assets/js/message'
import moment from "moment";

const app=createApp(App);//어플리케이션인스턴스생성 App.vue -> App.vue instance (Root Component)
app.config.globalProperties.message=message; //message 적용, globalProperties 전역변수적용
moment.locale("ja");//날짜 포맷 플러그인 언어 초기화
app.config.globalProperties.moment=moment;//날짜 포맷 플러그인 적용
app.use(store); // vuex의 store파일 적용, app.use() 플러그인사용
app.use(router); // router파일 적용
app.mount('#app') // App.vue instance -> index.html
