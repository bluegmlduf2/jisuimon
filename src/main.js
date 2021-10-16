import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import mitt from 'mitt'
import axios from 'axios'
import store from './store.js';
import router from './router.js';

const app=createApp(App);//어플리케이션인스턴스생성 App.vue -> App.vue instance (Root Component)
app.config.globalProperties.axios=axios;//글로벌 변수 적용부분 (axios등도 적용해주면 this.axios로 사용가능)
app.config.globalProperties.emitter=mitt(); //emitter 적용
app.use(store); // vuex의 store파일 적용
app.use(router); // router파일 적용
app.mount('#app') // App.vue instance -> index.html
