<template>
  <Nav />
  <Main />
</template>

<script>
import Main from './components/Main.vue'
import Nav from './components/Nav.vue'

export default {
  name: 'App',
  components: {
    Main:Main,
    Nav:Nav,
  }
}
</script>

<style>
@import "./assets/css/common.css"; /* 구글 머티리얼 아이콘 클래스,구글웹폰트 */

#app {
  font-family: 'M PLUS Rounded 1c', sans-serif!important;/* 구글 웹 폰트 */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: rgb(248, 249, 250);
  height: 100%;
}
@media (min-width: 992px){
  /* 넓이가 992px 이상 여백추가*/
  #app{
    padding-left:80px;
    padding-right:80px;
  }
}
</style>
