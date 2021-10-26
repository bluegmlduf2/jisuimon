<template>
  <nav class="navbar navbar-expand-md navbar-light fixed-top bg-light">
    <router-link class="navbar-brand" to="/">自炊モン</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <!-- 로그인 모바일 메뉴 -->
        <li class="nav-item nav_profile_mobile" v-if="profileShow">
          <a class="nav-link" href="#">My Post</a>
        </li>
        <li class="nav-item nav_profile_mobile" v-if="profileShow">
          <a class="nav-link" href="#">Setting</a>
        </li>
        <li class="nav-item nav_profile_mobile" v-if="profileShow">
          <a class="nav-link" href="#">Logout</a>
        </li>
      </ul>
      <form class="form-inline mt-2 mt-md-0">
        <input class="form-control mr-sm-4" id="searchMaterial" type="text" placeholder="食材を入力してください">
      </form>
        <!-- 로그인 메뉴 -->
        <button id="writePostBtn" v-if="profileShow" type="button" class="btn btn-light" @click="$router.push('/write')">New Post</button>
        <div class="nav_profile" v-if="profileShow">
          <div class="nav_profile_list" @click="profileMenuShow=!profileMenuShow">
            <img :src="require(`@/assets/img/faceMan1.jpg`)" alt="profileImg" />
            <span class="material-icons nav_profile_arrow">arrow_drop_down</span>
          </div>
          <div class="nav_profile_list_showBg" @click="profileMenuShow=!profileMenuShow" v-if="profileMenuShow">
            <div class="nav_profile_list_show" v-if="profileMenuShow">
              <router-link class="nav-link" to="#">My Post</router-link>
              <router-link class="nav-link" to="#">Setting</router-link>
              <router-link class="nav-link" to="#">Logout</router-link>
            </div>
          </div>
        </div>
    </div>
  </nav>
  <!-- 모바일 로그인 상태화면-->
  <!-- <div class="nav_profile_list_mobile" >
    <img :src="require(`@/assets/img/faceMan1.jpg`)" alt="profileImg" />
    <span class="material-icons nav_profile_arrow">arrow_drop_up</span>
  </div> -->
</template>

<script>
export default {
  name:"Nav",
  data() {
    return {
      profileShow:true, // 프로필 표시상태
      profileMenuShow:false // 프로필 메뉴표시상태
    }
  },
}
</script>

<style>
/* 넓이가 992px 이상 여백추가*/
@media (min-width: 992px){
  .navbar{
    padding-left:80px!important;
    padding-right:80px!important;
  }
}

.navbar-brand{
  color:rgb(96, 96, 96)!important;
  font-size:2rem!important;
}

.nav-item{
  font-size: 1.2rem;
}

.nav_profile img {
  height: 2.5rem;
  widows: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

/* 가로넓이가 최대767px까지 클래스적용 */
@media (max-width: 767px){
  .nav_profile{
    display: none;
  }
  #searchMaterial{
    width: 100%;
  }
  #writePostBtn{
    width: 100%;
    margin-top: 10px;
    border-radius:0.5rem!important;
  }
  .nav_profile_mobile{
    display: block!important;
  }
  .nav_profile_list_mobile{
    display: inline-block!important;
  }
}

#writePostBtn{
  font-weight: bold;
  margin-right: 0.7rem;
  padding-left: 1rem;
  padding-right: 1rem;
  font-size: 1rem;
  border-radius: 1rem;
  background: white;
  border: 1px solid rgb(96, 96, 96);
  color: rgb(96, 96, 96);
  transition: all 0.125s ease-in 0s;/* 마우스오버색상변환 */
  position: relative;/* list메뉴의 시작위치지정을 위해 추가 */
}

#writePostBtn:hover{
  background: rgb(52, 58, 64);
  color: white;
}

.nav_profile_list{
  display: inline-block;
  cursor: pointer;
}

.nav_profile_list_show{
    position: fixed;
    margin-top: 50px;
    width: 12rem;
    background: white;
    box-shadow: rgb(0 0 0 / 20%) 0px 0px 10px;
    right: 3.5rem;
}

.nav_profile_list_show > a{
  display: block;
  padding: 0.8rem 0;
  color: rgba(0,0,0,.9);
}

/* 모달닫기용 */
.nav_profile_list_showBg{
  background-color:transparent; 
  position:fixed;
  top:0;
  left:0;
  right:0;
  bottom:0;/** 모달배경을 꽉차게설정 top~bottom 0 설정이유 */
  padding:15px;
}

.nav_profile_arrow{
    position: relative;
    top: 6px;
}

.nav_profile_mobile{
  display: none;
}

/* 모바일 로그인 상태화면 (현재 사용하지않지만 나중에 게시물 좋아요 개발예정) */
.nav_profile_list_mobile{
  position: fixed;
  display: none;
  cursor: pointer;
  right: 1rem;
  bottom: 1rem;
  z-index: 1;/* 중첩요소중 가장앞에위치 */
}
.nav_profile_list_mobile img {
  height: 4rem;
  widows: 4rem;
  border-radius: 50%;
  object-fit: cover;
}
</style>