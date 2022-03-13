<template>
  <div class="commentCont">
    <h4>{{ comment.length }}件のコメント</h4>
    <div class="commentCont_write">
      <textarea
        class="form-control input_textarea"
        id="regCommentTa"
        placeholder="コメントを残してください"
        rows="3"
        v-model="inputComment"
        v-if="getLoginStatus"
      />
    </div>
    <div class="commentCont_reg" v-if="getLoginStatus">
      <button class="btn btn-success confirm_btn" id="regCommentBtn" @click="registerComment">
        <b>コメントを作成する</b>
      </button>
    </div>
    <!-- commentList -->
    <div class="commentCont_list">
      <div v-for="(comment,i) in comment" :key="comment.comment_id">
        <!-- 댓글 프로필 -->
        <div class="commentCont_list_profile">
          <div class="commentCont_profileImg">
            <img :src="`${comment.user_image}`" alt="profileImg">
          </div>
          <div class="commentCont_profileInfo update_button_cont">
            <div class="commentCont_profileInfo_name_cont">
              <div>
                <b>{{ comment.nickname }}</b>
              </div>
              <div class="commentCont_profileInfo_date">{{getCommentMoment(comment.comment_create_date)}}</div>
            </div>
            <div v-if="comment.comment_auth">
              <span @click="comment.updateState=true">修正</span>
              <span @click="deleteComment(comment.comment_id)">削除</span>
            </div>
          </div>
        </div>
        <!-- 댓글 코멘트 -->
        <div class="commentCont_list_content" v-if="comment.updateState">
          <textarea
            class="form-control input_textarea"
            placeholder="コメントを残してください"
            rows="3"
            ref="updateCommentInput"
            v-text="comment.comment_content"
          />
        </div>
        <div class="commentCont_list_content" v-else>
          {{ comment.comment_content }}
        </div>
        <div class="update_buttons" v-if="comment.updateState">
          <button class="btn btn-secondary cancel_btn" id="updateCommentCancelBtn" @click="comment.updateState=false" ><b>キャンセル</b></button>
          <button class="btn btn-success confirm_btn" id="updateCommentConfirmBtn" @click="updateComment(comment.comment_id)"><b>コメントを修正する</b></button>
        </div>
        <div class="commentCont_list_moreComment" >
          <span v-if="comment.showState" @click="comment.showState=false" class="material-icons commentCont_list_show">remove_circle_outline</span>
          <span v-else-if="comment.comment_reply.length>0 || getLoginStatus" @click="comment.showState=true" class="material-icons commentCont_list_hide">add_circle_outline</span>
          <span v-if="comment.comment_reply.length>0" @click="comment.showState=!comment.showState">&nbsp;{{comment.comment_reply.length+"件のコメント"}}</span>
          <span v-else-if="getLoginStatus" @click="comment.showState=!comment.showState">&nbsp;コメントを残す</span>
          <!-- nestedComment 대댓글 -->
          <div class="nestedCommentCont" :class="{'nestedComment_show': comment.showState,'nestedComment_hidden': !comment.showState }">
              <div class="nestedCommentCont_background">
                <div class="nestedCommentCont_hr" v-for="commentReply in comment.comment_reply" :key="commentReply.comment_reply_id">
                  <!-- 대댓글 프로필 -->
                  <div class="nestedCommentCont_profile">
                    <div class="commentCont_profileImg">
                      <img :src="`${commentReply.user_image_CR}`" alt="profileImg">
                    </div>
                    <div class="commentCont_profileInfo update_button_cont">
                      <div class="commentReplyCont_profileInfo_name_cont">
                        <div class="commentCont_profileInfo_name">
                          <b>{{ commentReply.nickname_CR }}</b>
                        </div>
                        <div class="commentCont_profileInfo_date">{{getCommentMoment(commentReply.comment_reply_create_date)}}</div>
                      </div>
                      <div v-if="commentReply.comment_reply_auth">
                        <span @click="commentReply.updateState=true">修正</span>
                        <span @click="deleteCommentReply(commentReply.comment_reply_id)">削除</span>
                      </div>
                    </div>
                  </div>
                  <!-- 대댓글 코멘트 -->
                  <div class="nestedCommentCont_comment" v-if="commentReply.updateState">
                    <textarea
                      class="form-control input_textarea"
                      placeholder="コメントを残してください"
                      rows="3"
                      ref="updateCommentReplyInput"
                      v-text="commentReply.comment_reply_content"
                    />
                  </div>
                  <div class="nestedCommentCont_comment" v-else>&emsp;{{commentReply.comment_reply_content}}</div>
                  <div class="update_buttons" v-if="commentReply.updateState">
                    <button class="btn btn-secondary cancel_btn" id="updateNestedCommentCancelBtn" @click="commentReply.updateState=false" ><b>キャンセル</b></button>
                    <button class="btn btn-success confirm_btn" id="updateNestedCommentConfirmBtn" @click="updateCommentReply(commentReply.comment_reply_id)"><b>コメントを修正する</b></button>
                  </div>
                </div>
                <!-- 대댓글 작성창 -->
                <div class="nestedCommentCont_newcomment" v-if="getLoginStatus">
                  <button id="writeNestedCommentBtn" v-if="comment.showReplyState" @click="comment.showReplyState=!comment.showReplyState" type="button" class="btn btn-outline-success confirm_white_btn"><b>コメント作成</b></button>
                  <div class="nestedCommentCont_write" v-if="!comment.showReplyState">
                    <textarea
                      class="form-control input_textarea"
                      id="regNewCommentTa"
                      placeholder="コメントを残してください"
                      rows="3"
                      v-model="inputCommentReply[i]"
                    />
                  </div>
                  <div class="nestedCommentCont_write_buttons" v-if="!comment.showReplyState">
                    <button class="btn btn-secondary cancel_btn" id="writeNestedCommentCancelBtn" @click="comment.showReplyState=!comment.showReplyState" ><b>キャンセル</b></button>
                    <button class="btn btn-success confirm_btn" id="writeNestedCommentConfirmBtn" @click="registerCommentReply(comment.comment_id,inputCommentReply[i])"><b>コメントを作成する</b></button>
                  </div>
                </div>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import common from "@/assets/js/common.js";

export default {
  name: "Comment",
  mixins: [common],
  props: {
    comment: Object,
    postId: String,
  },
  data() {
    return {
      inputComment: "", // 댓글내용
      inputCommentReply: [], // 대댓글내용 (v-for의 동적 v-model)
      updateShowState: false,
    };
  },
  computed: {
    // 로그인 상태 반환
    getLoginStatus() {
      return this.$store.getters["isSignedIn"];
    },
  },
  methods: {
    // 댓글용 시간 반환
    getCommentMoment(date) {
      const FROM_DATE = this.$moment(new Date()); // 현재시간
      const TO_DATE = this.$moment(date); // 비교시간
      const DAY_BETWEEN = FROM_DATE.diff(TO_DATE, "days"); // 비교일수

      // 비교일수가 1일이상일 경우에 일자까지만 표시, 1일 이내일 경우엔 현재기준으로 차이를 표시
      if (DAY_BETWEEN) {
        return this.$moment(date.comment_reply_create_date).format(
          "YYYY年 MM月 DD日"
        );
      } else {
        return this.$moment(TO_DATE).fromNow();
      }
    },
    // 댓글등록
    registerComment() {
      const COMMENT_CONTENT = this.inputComment; // 입력댓글

      // 입력값의 유효성체크
      if (!COMMENT_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false;
      }

      // 글자수 유효성검사
      if (!this.checkLength(COMMENT_CONTENT, 1000)) {
        this.$message.warningMessage(
          `コメントは最大${1000}文字まで入力できます`
        );
        return;
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = {
        method: "post",
        sendData: {
          postId: this.postId,
          commentContent: COMMENT_CONTENT,
        },
      };

      this.$store.commit("showSpinner");

      this.$store
        .dispatch("comment", payload)
        .then(() => {
          this.$message.successMessage("register").then(() => {
            this.$emit("updateCommentProps"); // props 다시 받아오기
            this.inputComment = ""; // 입력댓글초기화
          });
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit("hideSpinner");
        });
    },
    // 댓글수정
    updateComment(commentId) {
      const COMMENT_ID = commentId; // 댓글ID
      const COMMENT_CONTENT = this.$refs.updateCommentInput.value; // 사용자 작성 댓글

      // 댓글이 공백일시 유효성 검사
      if (!COMMENT_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false;
      }

      // 글자수 유효성검사
      if (!this.checkLength(COMMENT_CONTENT, 1000)) {
        this.$message.warningMessage(
          `コメントは最大${1000}文字まで入力できます`
        );
        return;
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = {
        method: "patch",
        sendData: {
          commentId: COMMENT_ID,
          commentContent: COMMENT_CONTENT
        },
      };
      this.$store.commit("showSpinner"); // 요청대기스피너 보기

      this.$store
        .dispatch("comment", payload)
        .then(() => {
          this.$message.successMessage("update").then(() => {
            this.$emit("updateCommentProps"); // props 다시 받아오기
            this.inputComment = ""; // 입력댓글초기화
            this.inputCommentReply = []; // 입력대댓글초기화
          });
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 댓글삭제
    deleteComment(commentId) {
      this.$message.confirmMessage("コメントを削除しますか?").then((res) => {
        // 확인버튼을 눌렀을시
        if (res.isConfirmed) {
          const COMMENT_ID = commentId; // 댓글ID

          // 입력정보를 서버전송데이터에 넣음
          const payload = {
            method: "delete",
            sendData: {
              commentId: COMMENT_ID,
            },
          };
          this.$store.commit("showSpinner"); // 요청대기스피너 보기

          this.$store
            .dispatch("comment", payload)
            .then(() => {
              this.$message.successMessage("delete").then(() => {
                this.$emit("updateCommentProps"); // props 다시 받아오기
                this.inputComment = ""; // 입력댓글초기화
                this.inputCommentReply = []; // 입력대댓글초기화
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
    // 대댓글등록
    registerCommentReply(commentId, commentReplyContent) {
      const COMMENT_ID = commentId; // 댓글ID
      const COMMENT_REPLY_CONTENT = commentReplyContent; // 대댓글내용

      // 입력값의 유효성체크
      if (!COMMENT_REPLY_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false;
      }

      // 글자수 유효성검사
      if (!this.checkLength(COMMENT_REPLY_CONTENT, 1000)) {
        this.$message.warningMessage(
          `コメントは最大${1000}文字まで入力できます`
        );
        return;
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = {
        method: "post",
        sendData: {
          commentId: COMMENT_ID,
          commentReplyContent: COMMENT_REPLY_CONTENT,
        },
      };

      this.$store.commit("showSpinner"); // 요청대기스피너 보기

      this.$store
        .dispatch("commentReply", payload)
        .then(() => {
          this.$message.successMessage("register").then(() => {
            this.$emit("updateCommentProps"); // props 다시 받아오기
            this.inputCommentReply = []; // 입력대댓글초기화
          });
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 대댓글수정
    updateCommentReply(commentReplyId) {
      const COMMENT_REPLY_ID = commentReplyId; // 대댓글ID
      const COMMENT_REPLY_CONTENT = this.$refs.updateCommentReplyInput.value; // 사용자 작성 대댓글

      // 댓글이 공백일시 유효성 검사
      if (!COMMENT_REPLY_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false;
      }

      // 글자수 유효성검사
      if (!this.checkLength(COMMENT_REPLY_CONTENT, 1000)) {
        this.$message.warningMessage(
          `コメントは最大${1000}文字まで入力できます`
        );
        return;
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = {
        method: "patch",
        sendData: {
          commentReplyId: COMMENT_REPLY_ID,
          commentReplyContent: COMMENT_REPLY_CONTENT,
        },
      };
      this.$store.commit("showSpinner"); // 요청대기스피너 보기

      this.$store
        .dispatch("commentReply", payload)
        .then(() => {
          this.$message.successMessage("update").then(() => {
            this.$emit("updateCommentProps"); // props 다시 받아오기
            this.inputComment = ""; // 입력댓글초기화
            this.inputCommentReply = []; // 입력대댓글초기화
          });
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit("hideSpinner"); // 요청대기스피너 보지않기
        });
    },
    // 대댓글삭제
    deleteCommentReply(commentReplyId) {
      this.$message.confirmMessage("コメントを削除しますか?").then((res) => {
        // 확인버튼을 눌렀을시
        if (res.isConfirmed) {
          const COMMENT_REPLY_ID = commentReplyId; // 대댓글ID

          // 입력정보를 서버전송데이터에 넣음
          const payload = {
            method: "delete",
            sendData: {
              commentReplyId: COMMENT_REPLY_ID,
            },
          };
          this.$store.commit("showSpinner"); // 요청대기스피너 보기

          this.$store
            .dispatch("commentReply", payload)
            .then(() => {
              this.$message.successMessage("delete").then(() => {
                this.$emit("updateCommentProps"); // props 다시 받아오기
                this.inputComment = ""; // 입력댓글초기화
                this.inputCommentReply = []; // 입력대댓글초기화
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
.commentCont h4 {
  margin-bottom: 20px;
}
.commentCont_write {
  margin-bottom: 20px;
}
.commentCont_reg {
  display: flex;
}
#regCommentBtn {
  margin-left: auto; /* flex의 왼쪽정렬 */
}
.commentCont_list_profile {
  display: flex; /* 자식 div자측정렬 */
}
.commentCont_list {
  padding-top: 0.5rem;
}
.commentCont_list > div {
  margin-top: 1rem;
}
.commentCont_list > div:not(:last-of-type) {
  border-bottom: 1px solid rgb(233, 236, 239);
}
.commentCont_profileImg > img {
  height: 2.5rem;
  width: 2.5rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}
.commentCont_profileInfo {
  padding-left: 0.7rem;
}
.commentCont_profileInfo_date {
  font-size: 0.75rem;
  color: rgb(134, 142, 150);
}
.update_button_cont {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.update_button_cont span {
  padding: 0px;
  outline: none;
  border: none;
  background: none;
  font-size: inherit;
  cursor: pointer;
  color: rgb(134, 142, 150);
  margin-left: 0.5rem;
  font-size: 0.8rem;
}
.commentCont_list_content {
  padding: 1rem 0 2rem;
  word-break: break-all;
}
.commentCont_list_moreComment {
  padding-bottom: 1.5rem;
}
.commentCont_list_moreComment > span {
  color: rgb(18, 184, 134);
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
}
.commentCont_list_show,
.commentCont_list_hide {
  position: relative;
  top: 2px;
}
.nestedComment_show {
  display: block;
}
.nestedComment_hidden {
  display: none;
}
.nestedCommentCont_background {
  border: 1px solid rgba(0, 0, 0, 0.02);
  background-color: rgba(0, 0, 0, 0.016);
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.3125rem;
}
.nestedCommentCont_hr {
  margin-bottom: 1rem;
  border-bottom: 1px solid rgb(233, 236, 239);
}
.nestedCommentCont_profile {
  display: flex; /* 자식 div자측정렬,flex의 default가 행정렬 */
  padding-bottom: 1.5rem;
}
.nestedCommentCont_comment {
  margin-bottom: 1.7rem;
  word-break: break-all;
}
#writeNestedCommentBtn {
  width: 100%;
}
.nestedCommentCont_write {
  margin-bottom: 20px;
}
.nestedCommentCont_write_buttons {
  display: flex;
  justify-content: flex-end;
}
#writeNestedCommentCancelBtn {
  margin-right: 0.7rem;
}
.update_buttons {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.5rem;
}
.update_buttons button {
  top: -0.7rem;
  position: relative;
}
.update_buttons .cancel_btn {
  margin-right: 0.7rem;
}
.commentCont_profileInfo_name_cont{
  max-width: 140px;
}
/* 메인 레이아웃 css (부트스트랩 스마트폰 가로 기준(576px미만) 으로 작성)*/
@media (max-width: 576.98px) {
  .commentReplyCont_profileInfo_name_cont{
    max-width: 110px;
  }
  .commentCont_profileInfo_name{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>