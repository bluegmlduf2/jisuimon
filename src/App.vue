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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: rgb(248, 249, 250);
  height: 100vh;
}
@media (min-width: 992px){
  /* 넓이가 992px 이상 여백추가*/
  #app{
    padding-left:80px;
    padding-right:80px;
  }
}
</style>
