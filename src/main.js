import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import mitt from 'mitt'
import axios from 'axios'
import store from './store.js';

const app=createApp(App);
const emitter=mitt();
app.config.globalProperties.axios=axios;//글로벌 변수 적용부분 (axios등도 적용해주면 this.axios로 사용가능)
app.config.globalProperties.emitter=emitter; //emitter 적용
app.use(store); // vuex의 store파일 적용
createApp(App).mount('#app')
