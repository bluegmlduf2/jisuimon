<template>
  <main class="settingCont">
    <!-- 프로필사진 -->
    <div class="settingCont_photoCont">
      <div class="settingCont_photoCont_image">
        <img :src="require(`@/assets/img/jisuimonLogo.png`)" alt="profireImg">
      </div>
      <div class="settingCont_photoCont_button">
        <button id="profileImgUploadBtn" class="btn btn-success confirm_btn" type="button"><b>プロフィール画像変更</b></button>
        <button id="profileImgDeletedBtn" class="btn btn-success confirm_white_btn" type="button"><b>プロフィール画像削除</b></button>
      </div>
    </div>
    <!-- 닉네임 -->
    <div class="settingCont_nicknameCont">
      <div class="setting_input">
        <h3 class="setting_label">닉네임명</h3>
        <div class="setting_cont" v-if="!nickNameClicked">닉네임123(입력폼변경)</div>
        <input type="text" id="" class="setting_cont form-control" v-if="nickNameClicked" placeholder="入力してください">
        <div class="setting_update update_btn" v-if="!nickNameClicked" @click="nickNameClicked=!nickNameClicked">수정</div>
        <div class="setting_update btn btn-success confirm_btn" v-if="nickNameClicked" @click="nickNameClicked=!nickNameClicked">저장</div>
      </div>
      <div class="setting_desc">
        표시되는 닉네임입니다..
      </div>
    </div>
    <!-- 패스워드 -->
    <div class="settingCont_passwordCont">
      <div  class="setting_input">
        <h3 class="setting_label">패스워드</h3>
        <input type="password" class="setting_cont form-control" v-if="passWordClicked" placeholder="현재 비밀번호">
        <div class="setting_update update_btn only" v-if="!passWordClicked" @click="passWordClicked=!passWordClicked">수정</div>
        <div class="setting_update btn btn-success confirm_btn" v-if="passWordClicked" @click="passWordClicked=!passWordClicked">저장</div>
        <input type="password" class="setting_cont only form-control" v-if="passWordClicked" placeholder="새 비밀번호">
        <input type="password" class="setting_cont only form-control" v-if="passWordClicked" placeholder="새 비밀번호 확인">
      </div>
      <div class="setting_desc">
        8글자 숫자와 특수문자 ...
      </div>
    </div>
    <!-- 탈퇴처리 -->
    <div class="settingCont_deleteUser">
      <div  class="setting_input">
        <div class="setting_label">탈퇴처리</div>
        <div id="" class="delete_btn" type="button"><b>탈퇴</b></div>
      </div>
      <div class="setting_desc">
        글 다 삭제됨 복구안됨..
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: "Setting",
  data() {
    return {
      nickName:'', // 닉네임
      nickNameClicked:false, // 닉네임변경 유무
      passWordClicked:false, // 패스워드변경 유무
    }
  },
};
</script>

<style>
@media (min-width: 577px) {
  /* 현재 넓이가 577px이하 (모바일)*/
  .settingCont {
    padding-top: 10vh;
  }
}
.settingCont {
  display: flex;
  flex-direction: column;
  text-align: left;
  font-size: 1rem;
  max-width: 447px; /* 1px~447px표시 아무리큰화면이라도 447px까지표시 모바일은 1까지줄어듬 */
  margin-left: auto;
  margin-right: auto;
}
/* 프로필사진 */
.settingCont_photoCont {
  display: flex;
  height: 13.75rem;
  flex-direction: column;
  align-items: center;
}

.settingCont_photoCont_image {
  margin-bottom: 1.25rem;
}

.settingCont_photoCont_image > img {
  height: 8rem;
  width: 8rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}

.settingCont_photoCont_button > button {
  display: block;
}

.settingCont_photoCont_button > #profileImgUploadBtn {
  margin-bottom: 1.25rem;
}

/* 입력부분 공통 */
.setting_input [class^="setting"] {
  /* .setting_input 클래스의 자식중에 클래스명이 setting..로 시작되는 요소 */
  display: inline-block;
}

.setting_label {
  color: rgb(52, 58, 64);
  margin: 0px;
  font-size: 1.125rem;
  width: 20%;
  font-weight: bold;
}

.setting_cont {
  /* 항상 70%를 유지하지만 최대 1px~224px까지만 커진다 */
  width: 62%;
  margin-left: 1.5%;
  margin-right: 1.5%;
  max-width: 277px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  vertical-align:middle; /* overflow:hidden;으로 높낮이가 안맞는걸 해결 */
}

.setting_cont.only {
  /* 클래스의특정기능추가 */
  margin: 1.2rem 11.5% 0 21.5%
}

.setting_update {
  width: 15%;
  text-align: center;
}

.setting_update.only{
  margin-left: 65%;
}

.setting_desc {
  display: block;
  margin-top: 0.875rem;
  color: rgb(134, 142, 150);
  font-size: 0.875rem;
}

/* 닉네임 */
.settingCont_nicknameCont {
  padding: 4rem 0 1.5rem;
}

/* 비밀번호 */
.settingCont_passwordCont {
  padding: 1.5rem 0;
  border-top: 1px solid rgb(233, 236, 239);
}

/* 탈퇴처리 */
.settingCont_deleteUser {
  padding: 1.5rem 0;
  border-top: 1px solid rgb(233, 236, 239);
}

/* 삭제버튼 css */
.confirm_white_btn {
  border: none !important;
}

.confirm_white_btn:hover,
.confirm_white_btn:active {
  color: rgb(18, 184, 134) !important;
  background: rgb(195, 250, 232) !important;
}
</style>