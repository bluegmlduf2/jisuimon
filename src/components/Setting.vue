<template>
  <div class="settingCont">
    <div class="settingCont_photoCont">
      <div class="settingCont_photoCont_image">
        <img :src="require(`@/assets/img/jisuimonLogo.png`)" alt="profireImg">
      </div>
      <div class="settingCont_photoCont_button">
        <button id="profileImgUploadBtn" class="btn btn-success confirm_btn" type="button"><b>プロフィール画像変更</b></button>
        <button id="profileImgDeletedBtn" class="btn btn-success confirm_white_btn" type="button"><b>プロフィール画像削除</b></button>
      </div>
    </div>
    <div class="settingCont_nicknameCont">
      <div class="settingCont_input">
        <h3 class="settingCont_label">닉네임명</h3>
        <div class="settingCont_cont">닉네임123(입력폼변경)</div>
        <div class="settingCont_update update_btn">수정</div>
      </div>
      <div class="settingCont_desc">
        표시되는 닉네임입니다..
      </div>
    </div>
    <div class="settingCont_passwordCont">
      <div class="settingCont_input">
        <h3 class="settingCont_label">패스워드</h3>
        <div class="settingCont_cont">현재 비밀번호</div>
        <div class="settingCont_update update_btn">수정</div>
      </div>
      <div  class="settingCont_input">
        <div class="settingCont_label"></div>
        <div class="settingCont_cont settingCont_cont_pt">새 비밀번호(숨기기)</div>
        <div class="settingCont_update"></div>
      </div>
      <div  class="settingCont_input">
        <div class="settingCont_label"></div>
        <div class="settingCont_cont settingCont_cont_pt">새 비밀번호 확인(숨기기)</div>
        <div class="settingCont_update"></div>
      </div>
      <div class="settingCont_desc">
        8글자 숫자와 특수문자 ...
      </div>
    </div>
    <div class="settingCont_deleteUser">
      <div  class="settingCont_input">
        <div class="settingCont_label">탈퇴처리</div>
        <div class="settingCont_cont">
          <div id="" class="delete_btn" type="button"><b>탈퇴</b></div>
        </div>
      </div>
      <div class="settingCont_desc">
        글 다 삭제됨 복구안됨..
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Setting",
}
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
/* 프로필사진 */
.settingCont_photoCont{
  display: flex;
  height: 13.75rem;
  flex-direction: column;
  align-items: center;
}

.settingCont_photoCont_image{
  margin-bottom: 1.25rem;
}

.settingCont_photoCont_image > img{
  height: 8rem;
  width: 8rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}

.settingCont_photoCont_button > button{
  display: block;
}

.settingCont_photoCont_button > #profileImgUploadBtn{
 margin-bottom: 1.25rem; 
}

/* 입력부분 공통 */
.settingCont_input{
  display: flex;
}

.settingCont_label{
  flex: 2;
  color: rgb(52, 58, 64);
  margin: 0px;
  font-size: 1.125rem;
  width: 20%;
  font-weight: bold;
}

.settingCont_cont{
  flex: 7;
  font-size: 1rem;
}

.settingCont_cont_pt{
  padding-top: 1.2rem;
}

.settingCont_update{
  flex: 1;
  font-size: 1rem;
}

.settingCont_desc{
  display: block;
  margin-top: 0.875rem;
  color: rgb(134, 142, 150);
  font-size: 0.875rem;
}

/* 닉네임 */
.settingCont_nicknameCont {
  margin-top: 4rem;
  text-align: left;
  padding-bottom: 1.5rem;
}

/* 비밀번호 */
.settingCont_passwordCont {
  padding: 1.5rem 0;
  text-align: left;
  border-top: 1px solid rgb(233, 236, 239);
}

/* 탈퇴처리 */
.settingCont_deleteUser {
  padding: 1.5rem 0;
  text-align: left;
  border-top: 1px solid rgb(233, 236, 239);
}

/* 삭제버튼 css */
.confirm_white_btn{
  border: none!important;;
}
.confirm_white_btn:hover,.confirm_white_btn:active{
  color: rgb(18, 184, 134)!important;
  background: rgb(195, 250, 232)!important;
}
</style>