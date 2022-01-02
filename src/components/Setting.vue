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
        <div class="setting_cont">닉네임123(입력폼변경)</div>
        <div class="setting_update update_btn">수정</div>
      </div>
      <div class="setting_desc">
        표시되는 닉네임입니다..
      </div>
    </div>
    <!-- 패스워드 -->
    <div class="settingCont_passwordCont">
      <div  class="setting_input">
        <h3 class="setting_label">패스워드</h3>
        <div class="setting_cont">현재 비밀번호</div>
        <div class="setting_update update_btn">수정</div>
        <div class="setting_cont only">새 비밀번호(숨기기)</div>
        <div class="setting_cont only">새 비밀번호 확인(숨기기)</div>
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
};
</script>

<style>
@media (min-width: 577px) {
  /* 현재 넓이가 577px이상 */
  .settingCont {
    padding-top: 10vh;
  }
}
/* Post,Comment 공통 레이아웃 */
@media (min-width: 992px) {
  /* 넓이가 992px 이상 여백추가*/
  .settingCont {
    padding-left: 160px;
    padding-right: 160px;
    width: 768px;
    margin-left: auto;
    margin-right: auto;
  }
}
.settingCont {
  display: flex;
  flex-direction: column;
  text-align: left;
  font-size: 1rem;
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
  width: 70%;
}

.setting_cont.only {
  /* 클래스의특정기능추가 */
  padding: 1.2rem 10% 0 20%;
}

.setting_update {
  width: 10%;
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