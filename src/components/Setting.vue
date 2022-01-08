<template>
  <main class="settingCont">
    <!-- 프로필사진 -->
    <div class="settingCont_photoCont">
      <div class="settingCont_photoCont_image">
        <img :src="photoUrl" alt="profireImg">
      </div>
      <div class="settingCont_photoCont_button">
        <label for="profileImgUploadBtn" class="btn btn-success confirm_btn">
          <b>プロフィール画像変更</b>
        </label>
        <input id="profileImgUploadBtn" ref="profileImgUploadRef" accept="image/png,image/jpeg" type="file" @change="updateProfileImg">
        <button id="profileImgDeletedBtn" class="btn btn-success confirm_white_btn" type="button" @click="deleteProfileImg"><b>プロフィール画像削除</b></button>
      </div>
    </div>
    <!-- 닉네임 -->
    <div class="settingCont_nicknameCont">
      <div class="setting_input">
        <h3 class="setting_label">닉네임명</h3>
        <div class="setting_cont" v-if="!nickNameClicked">{{nickName}}</div>
        <input type="text" class="setting_cont form-control" v-model="nickNameUpdated" v-if="nickNameClicked" placeholder="入力してください">
        <div class="setting_update update_btn" v-if="!nickNameClicked" @click="nickNameClicked=!nickNameClicked">수정</div>
        <div class="setting_update btn btn-success confirm_btn" v-if="nickNameClicked" @click="updateNickName">저장</div>
      </div>
      <div class="setting_desc">
        표시되는 닉네임입니다..
      </div>
    </div>
    <!-- 패스워드 -->
    <div class="settingCont_passwordCont">
      <div  class="setting_input">
        <h3 class="setting_label">패스워드</h3>
        <input type="password" class="setting_cont form-control" v-if="passWordClicked" v-model="currentPassUpdated" placeholder="현재 비밀번호">
        <div class="setting_update update_btn only" v-if="!passWordClicked" @click="passWordClicked=!passWordClicked">수정</div>
        <div class="setting_update btn btn-success confirm_btn" v-if="passWordClicked" @click="updatePassword">저장</div>
        <input type="password" class="setting_cont only form-control" v-if="passWordClicked" v-model="newPassUpdated" placeholder="새 비밀번호">
        <input type="password" class="setting_cont only form-control" v-if="passWordClicked" v-model="newPassConfirmUpdated" placeholder="새 비밀번호 확인">
      </div>
      <div class="setting_desc">
        8글자 숫자와 특수문자 ...
      </div>
    </div>
    <!-- 탈퇴처리 -->
    <div class="settingCont_deleteUser">
      <div  class="setting_input">
        <div class="setting_label">탈퇴처리</div>
        <div id="" class="delete_btn" type="button" @click="deleteUser"><b>탈퇴</b></div>
      </div>
      <div class="setting_desc">
        글 다 삭제됨 복구안됨..
      </div>
    </div>
  </main>
</template>


<script>
import common from "@/assets/js/common.js";
import firebase from "@/firebase";

export default {
  name: "Setting",
  mixins: [common],
  data() {
    return {
      // 표시용
      photoUrl: "", // 프로필사진URL (표시용)
      nickName: "", // 닉네임 (표시용)
      // 갱신용
      photoUrlUpdated: "", // 프로필사진URL
      nickNameUpdated: "", // 닉네임
      currentPassUpdated: "", // 현재비밀번호
      newPassUpdated: "", // 새로운비밀번호
      newPassConfirmUpdated: "", // 새로운비밀번호확인
      // 화면상태
      nickNameClicked: false, // 닉네임변경 유무
      passWordClicked: false, // 패스워드변경 유무
    };
  },
  created() {
    this.initUser(); // 파이어베이스 유저 초기화
  },
  methods: {
    // 파이어베이스 유저정보 현재화면에 초기화
    initUser() {
      // 유저정보
      this.photoUrl = firebase.getUserInfo().PHOTO_URL;
      this.nickName = firebase.getUserInfo().DISP_NAME;
      // 인풋초기화
      this.photoUrlUpdated = ""; // 프로필사진인풋 초기화
      this.nickNameUpdated = ""; // 닉네임인풋 초기화
      this.currentPassUpdated = ""; // 현재비밀번호
      this.newPassUpdated = ""; // 새로운비밀번호
      this.newPassConfirmUpdated = ""; // 새로운비밀번호확인
    },
    // 유저 프로필 변경
    updateProfileImg(event) {      
      // 파일정보
      const FILE = event?.target.files[0],
        FILE_NAME = FILE?.name,
        IDXDOT = FILE_NAME?.lastIndexOf(".") + 1,
        EXT_FILE = FILE_NAME?.substr(IDXDOT, FILE_NAME.length).toLowerCase();

      //이미지 파일형식체크와 공백체크 유효성검사
      if (!["jpg", "jpeg", "png"].includes(EXT_FILE) || !FILE_NAME) {
        this.$message.warningMessage(
          "イメージファイルをアップロードしてください。"
        );
        return;
      }

      // 파일전송객체
      const formData = new FormData();
      formData.append("userImage", FILE);

      //전송할데이터
      const payload = {
        method: "post",
        sendData: formData,
      };

      this.$store
        .dispatch("userImage", payload, true)
        .then(() => {
          this.$message
            .successMessage("TODOプロフィール写真変更しました。")
            .then(async () => {
              // 파이어베이스의 현재유저정보 초기화 initUser함수에 배치시 초기화느림
              await firebase.auth.currentUser.reload();
              this.initUser(); // 유저정보초기화
            });
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$refs.profileImgUploadRef.value=null; // 동일한 이름의 파일선택시 change이벤트 발생이 안되는 버그대비
          this.loading = false;
        });
    },
    // 유저 프로필 삭제
    deleteProfileImg() {
      this.$message.confirmMessage("TODO削除する？").then((res) => {
        // 확인버튼을 눌렀을시
        if (res.isConfirmed) {
          this.loading = true;
          const payload = {
            method: "delete",
          };
          this.$store
            .dispatch("userImage", payload)
            .then(() => {
              this.$message
                .successMessage("TODOプロフィール写真変更しました。")
                .then(async () => {
                  // 파이어베이스의 현재유저정보 초기화 initUser함수에 배치시 초기화느림
                  await firebase.auth.currentUser.reload();
                  this.initUser(); // 유저정보초기화
                });
            })
            .catch((err) => {
              this.$message.errorMessage(err);
            })
            .finally(() => {
              this.$refs.profileImgUploadRef.value=null; // 동일한 이름의 파일선택시 change이벤트 발생이 안되는 버그대비
              this.loading = false;
            });
        }
      });
    },
    // 유저 닉네임 변경
    updateNickName() {
      // TODO 유효성체크 닉네임

      // TODO 닉네임변경란이 공백이고 저장클릭시 변경안하고 그냥 현재 input모드 닫기

      // 업데이트할 유저정보
      const UPDATE_INFO = {
        flag: "nickName",
        nickName: this.nickNameUpdated,
      };

      firebase
        .updateUser(UPDATE_INFO)
        .then((res) => {
          this.$message.okMessage(res, false);
        })
        .catch((err) => {
          this.$message.warningMessage(err.message);
        })
        .finally(() => {
          this.nickNameClicked = !this.nickNameClicked; // 버튼상태변경
          this.initUser(); // 유저정보초기화
        });
    },
    // 유저 비밀번호 변경
    updatePassword() {
      // TODO 유효성체크 비밀번호 일치,글자수,특문포함여부

      // TODO 현재비밀번호,새비밀번호,새비밀번호확인 란이 공백이고 저장클릭시 변경안하고 그냥 현재 input모드 닫기

      // 업데이트할 유저정보
      const UPDATE_INFO = {
        currentPassword: this.currentPassUpdated,
        newPassword: this.newPassUpdated,
      };

      firebase
        .updatePass(UPDATE_INFO)
        .then((res) => {
          this.$message.okMessage(res, false);
        })
        .catch((err) => {
          this.$message.warningMessage(err.message);
        })
        .finally(() => {
          this.passWordClicked = !this.passWordClicked; // 버튼상태변경
          this.initUser(); // 유저정보초기화
        });
    },
    // 유저삭제
    deleteUser() {
      this.$message.confirmMessage("TODO削除する？").then((res) => {
        // 확인버튼을 눌렀을시
        if (res.isConfirmed) {
          this.loading = true;
          const payload = {
            method: "delete",
          };
          this.$store
            .dispatch("deleteUser", payload)
            .then(() => {
              this.$message
                .successMessage(
                  "TODO脱会処理しました。\nご利用ありがとうございました。"
                )
                .then(() => {
                  // 탈퇴후 홈화면으로 이동
                  const HOME_URL = `/${location.pathname.split("/")[1]}`;
                  window.location.href = HOME_URL;
                });
            })
            .catch((err) => {
              this.$message.errorMessage(err);
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
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

.settingCont_photoCont_button > label[for="profileImgUploadBtn"] {
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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle; /* overflow:hidden;으로 높낮이가 안맞는걸 해결 */
}

.setting_cont.only {
  /* 클래스의특정기능추가 */
  margin: 1.2rem 11.5% 0 21.5%;
}

.setting_update {
  width: 15%;
  text-align: center;
}

.setting_update.only {
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
  margin: 4rem 0 1.5rem;
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