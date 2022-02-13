<template>
  <main class="settingCont">
    <!-- 프로필사진 -->
    <div class="settingCont_photoCont">
      <div class="settingCont_photoCont_image">
        <img :src="photoUrl" alt="profireImg" />
      </div>
      <div class="settingCont_photoCont_button">
        <label for="profileImgUploadBtn" class="btn btn-success confirm_btn">
          <b>プロフィール画像変更</b>
        </label>
        <input
          id="profileImgUploadBtn"
          ref="profileImgUploadRef"
          accept="image/png,image/jpeg"
          type="file"
          @change="updateProfileImg"
        />
        <button
          id="profileImgDeletedBtn"
          class="btn btn-success confirm_white_btn"
          type="button"
          @click="deleteProfileImg"
        >
          <b>プロフィール画像削除</b>
        </button>
      </div>
    </div>
    <!-- 닉네임 -->
    <div class="settingCont_nicknameCont">
      <div class="setting_input">
        <h3 class="setting_label">ニックネーム</h3>
        <div class="setting_cont" v-if="!nickNameClicked">{{ nickName }}</div>
        <input
          type="text"
          class="setting_cont form-control"
          v-model="nickNameUpdated"
          v-if="nickNameClicked"
          placeholder="入力してください"
        />
        <div
          class="setting_update update_btn"
          v-if="!nickNameClicked"
          @click="nickNameClicked = !nickNameClicked"
        >
          変更
        </div>
        <div
          class="setting_update btn btn-success confirm_btn"
          v-if="nickNameClicked"
          @click="updateNickName"
        >
          <b>保存</b>
        </div>
      </div>
      <div class="setting_desc">表示されるニックネームです</div>
    </div>
    <!-- 패스워드 -->
    <div class="settingCont_passwordCont">
      <div class="setting_input">
        <h3 class="setting_label">パスワード</h3>
        <input
          type="password"
          class="setting_cont form-control"
          v-if="passWordClicked"
          v-model="currentPassUpdated"
          placeholder="現在のパスワード"
        />
        <div
          class="setting_update update_btn only"
          v-if="!passWordClicked"
          @click="passWordClicked = !passWordClicked"
        >
          変更
        </div>
        <div
          class="setting_update btn btn-success confirm_btn"
          v-if="passWordClicked"
          @click="updatePassword"
        >
          <b>保存</b>
        </div>
        <input
          type="password"
          class="setting_cont only form-control"
          v-if="passWordClicked"
          v-model="newPassUpdated"
          placeholder="新しいパスワード"
        />
        <input
          type="password"
          class="setting_cont only form-control"
          v-if="passWordClicked"
          v-model="newPassConfirmUpdated"
          placeholder="新しいパスワード再入力"
        />
      </div>
      <div class="setting_desc">
        半角英数字、記号1文字以上使用、全体で8文字以上を入力してください
      </div>
    </div>
    <!-- 탈퇴처리 -->
    <div class="settingCont_deleteUser">
      <div class="setting_input">
        <div class="setting_label">脱退処理</div>
        <div id="" class="delete_btn" type="button" @click="deleteUser">
          <b>脱退</b>
        </div>
      </div>
      <div class="setting_desc">
        脱退したらアカウントを元に戻すことが出来ません
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

      this.$store.commit("showSpinner"); // 요청대기스피너 보기

      this.$store
        .dispatch("userImage", payload, true)
        .then(() => {
          this.$message
            .successMessage("update", "プロフィール写真変更しました")
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
          this.$refs.profileImgUploadRef.value = null; // 동일한 이름의 파일선택시 change이벤트 발생이 안되는 버그대비
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 유저 프로필 삭제
    deleteProfileImg() {
      this.$message
        .confirmMessage("プロフィール写真を削除しますか?")
        .then((res) => {
          // 확인버튼을 눌렀을시
          if (res.isConfirmed) {
            const payload = {
              method: "delete",
            };
            this.$store.commit("showSpinner"); // 요청대기스피너 보기
            this.$store
              .dispatch("userImage", payload)
              .then(() => {
                this.$message
                  .successMessage("delete", "プロフィール写真を削除しました。")
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
                this.$refs.profileImgUploadRef.value = null; // 동일한 이름의 파일선택시 change이벤트 발생이 안되는 버그대비
                this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
              });
          }
        });
    },
    // 유저 닉네임 변경
    updateNickName() {
      // 닉네임변경란이 공백이고 저장클릭시 변경안하고 그냥 현재 input모드 닫기
      if (!this.nickNameUpdated) {
        this.nickNameClicked = false; // 닉네임변경 유무
        return;
      }

      // 글자수 유효성
      if (!this.checkLength(this.nickNameUpdated, 30)) {
        this.$message.warningMessage(
          `ニックネームは最大${30}文字まで入力できます`
        );
        return;
      }

      // 업데이트할 유저정보
      const UPDATE_INFO = {
        flag: "nickName",
        nickName: this.nickNameUpdated,
      };

      this.$store.commit("showSpinner"); // 요청대기스피너 보기

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
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 유저 비밀번호 변경
    updatePassword() {
      // 현재비밀번호,새비밀번호,새비밀번호확인 란이 공백이고 저장클릭시 변경안하고 그냥 현재 input모드 닫기
      if (
        !this.currentPassUpdated &&
        !this.newPassUpdated &&
        !this.newPassConfirmUpdated
      ) {
        this.passWordClicked = false; // 패스워드변경 유무
        return;
      }

      // 비밀번호의 유효성 확인
      if (!this.checkPass(this.currentPassUpdated)) {
        this.$message.warningMessage(
          "現在のパスワードを半角英数字、記号1文字以上使用、全体で8文字以上を入力してください"
        );
        return;
      }
      // 비밀번호의 유효성 확인
      if (!this.checkPass(this.newPassUpdated)) {
        this.$message.warningMessage(
          "新しいパスワードを半角英数字、記号1文字以上使用、全体で8文字以上を入力してください"
        );
        return;
      }
      // 비밀번호의 유효성 확인
      if (!this.checkPass(this.newPassConfirmUpdated)) {
        this.$message.warningMessage(
          "再入力パスワードを半角英数字、記号1文字以上使用、全体で8文字以上を入力してください"
        );
        return;
      }

      // 모든 문자열이 같은지 체크 (첫번째 배열 인수와 나머지 인수가 모두 일치하는지 체크)
      const PASS_EQUAL_CHECK = [
        this.newPassUpdated,
        this.newPassConfirmUpdated,
      ].every((val, i, arr) => val === arr[0]);
      
      if (!PASS_EQUAL_CHECK) {
        this.$message.warningMessage("再パスワードが一致しません");
        return;
      }

      // 업데이트할 유저정보
      const UPDATE_INFO = {
        currentPassword: this.currentPassUpdated,
        newPassword: this.newPassUpdated,
      };

      this.$store.commit("showSpinner"); // 요청대기스피너 보기

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
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 유저삭제
    deleteUser() {
      this.$message.confirmMessage("脱退しますか?").then((res) => {
        // 확인버튼을 눌렀을시
        if (res.isConfirmed) {
          const payload = {
            method: "delete",
          };
          this.$store.commit("showSpinner"); // 요청대기스피너 보기

          this.$store
            .dispatch("deleteUser", payload)
            .then(() => {
              this.$message
                .successMessage(
                  "delete",
                  "脱退処理しました。\nご利用ありがとうございました。"
                )
                .then(() => {
                  // 탈퇴후 홈화면으로 이동
                  this.moveToHome();
                });
            })
            .catch((err) => {
              this.$message.errorMessage(err);
            })
            .finally(() => {
              this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
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
  font-size: 0.9rem;
  width: 27%;
  font-weight: bold;
}

.setting_cont {
  /* 항상 70%를 유지하지만 최대 1px~224px까지만 커진다 */
  width: 53%;
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
  margin: 1.2rem 11.5% 0 28.5%;
}

.setting_update {
  width: 17%;
  text-align: center;
}

.setting_update.only {
  margin-left: 56%;
}

.setting_desc {
  display: block;
  margin-top: 0.835rem;
  color: rgb(134, 142, 150);
  font-size: 0.835rem;
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