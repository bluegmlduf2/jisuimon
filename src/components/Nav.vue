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
        <button id="writePostBtn" v-if="profileShow" type="button" class="btn btn-light" @click="isLogin?$router.push('/write'):loginShow=true">{{isLogin?"New Post":"Login"}}</button>
        <div class="nav_profile" v-if="profileShow && isLogin">
          <div class="nav_profile_list" @click="profileMenuShow=!profileMenuShow">
            <!-- <img :src="require(`@/static/img/faceMan1.jpg`)" alt="profileImg" /> -->
            <span class="material-icons nav_profile_arrow">arrow_drop_down</span>
          </div>
          <div class="nav_profile_list_showBg" @click="profileMenuShow=!profileMenuShow" v-if="profileMenuShow">
            <div class="nav_profile_list_show" v-if="profileMenuShow">
              <router-link class="nav-link" to="#">My Post</router-link>
              <router-link class="nav-link" to="#">Setting</router-link>
              <router-link class="nav-link" @click="logout" to="#">Logout</router-link>
            </div>
          </div>
        </div>
    </div>
  </nav>
  <!-- 로그인 팝업 (TODO 나중에 컴포넌트분리필요)-->
  <!-- <div class="loginCont_showBg"> -->
  <div class="loginCont_showBg" v-if="loginShow">
    <div class="loginCont">
      <div class="loginCont_welcome">
        <img :src="require(`@/assets/img/jisuimonLogo.png`)" alt="">
        <h4>自炊モンに<br>ようこそ</h4>
      </div>
      <div class="loginCont_login">
        <div class="loginCont_exit">
          <span class="material-icons" id="loginClose" @click="closeLoginForm">close</span>
        </div>
        <div class="loginCont_main">
          <div class="loginCont_body">
            <h2><b>{{signUpShow?"会員登録":"ログイン"}}</b></h2>
            <h4>{{signUpShow?"メールアドレスで会員登録":"メールアドレスでログイン"}}</h4>
            <div class="loginCont_body_input">
              <input type="text" id="loginEmailInput" v-model="userEmail" 
                class="form-control" :class="{'is-invalid': validationEmailCheck}" placeholder="メールアドレスを入力してください" required>
              <div class="invalid-feedback" for="loginEmailInput" v-if="validationEmailCheck">メールアドレスの形式を確認してください</div>
              <input type="password" id="loginPassWordInput" v-model="userPass"
                class="form-control" :class="{'is-invalid': validationPassCheck}" placeholder="パスワードを入力してください" required>
              <div class="invalid-feedback" for="loginPassWordInput" v-if="validationPassCheck">半角英数字のみ、記号1文字以上使用、全体で8文字以上を入力してください</div>
              <button class="btn btn-success confirm_btn" id="loginBtn" @click="signUpShow?signup():login()"><b>{{signUpShow?"会員登録":"ログイン"}}</b></button>
            </div>
          </div>
          <div class="loginCont_footer">
            {{signUpShow?"既にメンバーの方は、":"まだメンバーでない方は、"}}
            <span id="moveSignUpBtn" @click="showSignUpForm">こちらから</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- 모바일 로그인 상태화면-->
  <!-- <div class="nav_profile_list_mobile" >
    <img src="https://placeimg.com/100/100/arch" alt="profileImg" />
    <span class="material-icons nav_profile_arrow">arrow_drop_up</span>
  </div> -->
</template>

<script>
import common from "@/assets/js/common.js";
import firebase from '@/firebase';

export default {
  name:"Nav",
  mixins: [common],
  data() {
    return {
      userEmail:'',
      userPass:'',
      loginShow:false, // 로그인창 표시 유무
      signUpShow:false, // 회원가입창 표시 유무
      validationUserEmail:false, // 이메일 유효성
      validationUserPass:false, // 패스워드 유효성
      afterValidation:false, // 최초 로그인부터 유효성검사
      profileShow:true, // 프로필 표시상태
      profileMenuShow:false // 프로필 메뉴표시상태
    }
  },
  created(){
    // TODO삭제예정(테스트유저입력용)
    this.userEmail="blue@nate.com"
    this.userPass="111111"
  },
  methods: {
    // 로그인
    login(){
      this.afterValidation=true
      //TODO 1.원형프로그레스 , 유효성체크
      firebase.signInWithEmailAndPassword(this.userEmail, this.userPass).then(
        (res) => {
          this.closeLoginForm(); // 로그인 창 닫기
          this.$message.okMessage(res,false);
        }
      ).catch((err)=>{
        this.$message.warningMessage(err.message);
      })
    },
    // 로그아웃
    logout(){
      firebase.logout().then((res) => {
        this.$message.okMessage(res,false);
      }).catch((err) => {
        this.$message.warningMessage(err.message);
      }).finally(() => {
        this.$router.push('/')
      });
    },
    // 회원가입
    signup(){
      this.afterValidation=true
      //TODO 1.원형프로그레스 , 유효성체크
      firebase.signUpWithEmailAndPassword(this.userEmail, this.userPass).then(
        (res) => {
          this.closeLoginForm(); // 로그인 창 닫기
          this.$message.okMessage(res,false);
        }
      ).catch((err)=>{
        this.$message.warningMessage(err.message);
      })
    },
    // 로그인창 표시
    showLoginForm(){
      this.loginShow=true; // 로그인창 표시
    },
    // 회원등록창 표시
    showSignUpForm(){
      this.afterValidation=false; // 유효성 검사유무
      this.validationUserEmail=false; // 이메일 유효성
      this.validationUserPass=false; // 패스워드 유효성
      this.signUpShow=!this.signUpShow // 회원등록창 표시
    },
    // 로그인창 닫기
    closeLoginForm(){
      // 입력폼 초기화
      this.userEmail="";
      this.userPass="";
      // 유효성 초기화
      this.afterValidation=false; // 유효성 검사유무
      this.validationUserEmail=false; // 이메일 유효성
      this.validationUserPass=false; // 패스워드 유효성
      this.signUpShow=false; // 로그인화면 변경
      this.loginShow=false; // 로그인창 닫기
    }
  },
  computed: {
    // 로그인상태반환
    isLogin(){
      return this.$store.getters['isSignedIn']
    },
    // 이메일 폼체크
    validationEmailCheck(){
      return !this.validationUserEmail&&this.afterValidation 
    },
    // 패스워드 폼체크
    validationPassCheck(){
      return !this.validationUserPass&&this.afterValidation 
    }
  },
  watch:{
    // 이메일 유효성체크
    userEmail(inputEmail){
      this.validationUserEmail=this.checkEmail(inputEmail)
    },
    // 패스워드 유효성체크
    userPass(inputPass) {
      this.validationUserPass=this.checkPass(inputPass)
    }
  }
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

/* 로그인 팝업 배경 */
.loginCont_showBg{
  background-color:rgba(249, 249, 249, 0.85);; 
  position:fixed;
  top:0;
  left:0;
  right:0;
  bottom:0;/* 모달배경을 꽉차게설정 top~bottom 0 설정이유 */
  width: 100%;
  z-index: 9999;
  display: flex;/* 아래는 플렉스를 이용한 가운데 정렬 */
  justify-content: center;
  align-items: center;
}
.loginCont{
  width: 606px;
  height: 480px;
  animation: 0.4s ease-in-out 0s 1 normal forwards running hwrkPK;
  box-shadow: rgb(0 0 0 / 9%) 0px 2px 12px 0px;
  display: flex;
}
.loginCont_welcome{
  width: 216px;
    background: rgb(241, 243, 245);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;/* 세로정렬 */
    align-items: center;
    justify-content: center;
    -webkit-box-pack: center;
    -webkit-box-align: center;
}

@media (max-width: 576.98px) {
  .loginCont{
    height: 100%;
  }
  .loginCont_welcome{
    display: none;
  }
}
.loginCont_welcome img{
  width: 100%;
  border-radius: 7px;
}
.loginCont_welcome h4{
    margin-top: 1.5rem;
    color: rgb(73, 80, 87);
    text-align: center;
    line-height:2rem;
}

.loginCont_login{
  flex: 1 1 0%;
  background: white;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.loginCont_exit{
  display: flex;
  justify-content: flex-end;
  color: rgb(134, 142, 150);
  margin-bottom: 2.25rem;
}

#loginClose{
  cursor: pointer;
}

.loginCont_main{
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* flex간 동일 간격을 줌 */
  flex: 1 1 0%; /* 플렉스의 자식이 크고 작을때에 상관없이 꽉찬하나의 행을 차지  */
}

.loginCont_body{
  text-align: left;
}

.loginCont_body h2{
  font-size: 1.3125rem;
  color: rgb(52, 58, 64);
}

.loginCont_body h4{
  font-size: initial; /* h4 폰트사이즈 초기화(상속막기) */
  margin-top: 1rem;
  margin-bottom: 1rem;
  color: rgb(134, 142, 150);
}

#loginEmailInput,#loginPassWordInput{
  height: 3rem;
  margin-top: 1rem;
}

.loginCont_body_input{
  height: 3rem;
}

#loginEmailInput::placeholder ,#loginPassWordInput::placeholder{
  font-size: 0.9rem;
}

#loginBtn{
  margin-top: 1.1rem;
  width: 100%;
}

.loginCont_footer{
  text-align: right;
}

#moveSignUpBtn{
  font-weight: bold;
  color: rgb(18, 184, 134);
  cursor: pointer;
}
</style>