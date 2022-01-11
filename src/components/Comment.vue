<template>
  <div class="commentCont">
    <h4>{{ comment.length }}件のコメント</h4>
    <div class="commentCont_write">
      <textarea
        class="form-control"
        id="regCommentTa"
        placeholder="コメントを残してください"
        rows="3"
        v-model="inputComment"
      />
    </div>
    <div class="commentCont_reg">
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
          <div class="commentCont_profileInfo">
            <div class="commentCont_profileInfo_name">
              <b>{{ comment.nickname }}</b>
            </div>
            <div class="commentCont_profileInfo_date">{{$moment(comment.comment_create_date).format("YYYY年 MM月 DD日 dddd  hh時 mm分")}}</div>
          </div>
        </div>
        <!-- 댓글 코멘트 -->
        <div class="commentCont_list_content">
          {{ comment.comment_content }}
        </div>
        <div class="commentCont_list_moreComment" >
          <span v-if="comment.showState" @click="comment.showState=!comment.showState" class="material-icons commentCont_list_show">remove_circle_outline</span>
          <span v-if="!comment.showState" @click="comment.showState=!comment.showState" class="material-icons commentCont_list_hide">add_circle_outline</span>
          <span @click="comment.showState=!comment.showState">&nbsp;{{comment.comment_reply.length>0?`${comment.comment_reply.length}件のコメント`:"コメントを残す"}}</span>
          <!-- nestedComment 대댓글 -->
          <div class="nestedCommentCont" :class="{'nestedComment_show': comment.showState,'nestedComment_hidden': !comment.showState }">
              <div class="nestedCommentCont_background">
                <div class="nestedCommentCont_hr" v-for="commentReply in comment.comment_reply" :key="commentReply.comment_reply_id">
                  <!-- 대댓글 프로필 -->
                  <div class="nestedCommentCont_profile">
                    <div class="commentCont_profileImg">
                      <img :src="`${commentReply.user_image_CR}`" alt="profileImg">
                    </div>
                    <div class="commentCont_profileInfo">
                      <div class="commentCont_profileInfo_name">
                        <b>{{ commentReply.nickname_CR }}</b>
                      </div>
                      <div class="commentCont_profileInfo_date">{{$moment(commentReply.comment_reply_create_date).format("YYYY年 MM月 DD日 dddd  hh時 mm分")}}</div>
                    </div>
                  </div>
                  <!-- 대댓글 코멘트 -->
                  <div class="nestedCommentCont_comment">&emsp;{{commentReply.comment_reply_content}}</div>
                </div>
                <!-- 대댓글 작성창 -->
                <div class="nestedCommentCont_newcomment">
                  <button id="writeNestedCommentBtn" v-if="comment.showReplyState" @click="comment.showReplyState=!comment.showReplyState" type="button" class="btn btn-outline-success confirm_white_btn"><b>コメント作成</b></button>
                  <div class="nestedCommentCont_write" v-if="!comment.showReplyState">
                    <textarea
                      class="form-control"
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

export default {
  name: "Comment",
  props: {
    comment: Object,
    postId: String,
  },
  data() {
    return {
      inputComment : "", // 댓글내용
      inputCommentReply : [], // 대댓글내용 (v-for의 동적 v-model)
    };
  },
  methods:{
    // 댓글등록
    registerComment(){
      const COMMENT_CONTENT=this.inputComment // 입력댓글

      // 입력값의 유효성체크
      if (!COMMENT_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = { 
        method: "post",
        sendData: {
          postId:this.postId,
          commentContent:COMMENT_CONTENT
        }
      };

      this.$store.commit('showSpinner');

      this.$store
        .dispatch("comment", payload)
        .then(() => {
          this.$message.successMessage().then(()=>{
            this.$emit('updateCommentProps') // props 다시 받아오기 
            this.inputComment="" // 입력댓글초기화
          })
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit('hideSpinner');
        });
    },
    // 대댓글등록
    registerCommentReply(commentId,commentReplyContent){
      const COMMENT_ID=commentId// 댓글ID
      const COMMENT_REPLY_CONTENT=commentReplyContent // 대댓글내용

      // 입력값의 유효성체크
      if (!COMMENT_REPLY_CONTENT) {
        this.$message.warningMessage("コメントを入力してください");
        return false
      }

      // 입력정보를 서버전송데이터에 넣음
      const payload = { 
        method: "post",
        sendData: {
          commentId:COMMENT_ID,
          commentReplyContent:COMMENT_REPLY_CONTENT
        }
      };

      this.$store.commit('showSpinner'); // 요청대기스피너 보기

      this.$store
        .dispatch("commentReply", payload)
        .then(() => {
          this.$message.successMessage().then(()=>{
            this.$emit('updateCommentProps') // props 다시 받아오기 
            this.inputComment="" // 입력댓글초기화
          })
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.$store.commit('hideSpinner'); // 요청대기스피너 보지않기
        });
    }
  }
};
</script>

<style>
.commentCont h4 {
  margin-bottom: 20px;
}
.commentCont_write {
  margin-bottom: 20px;
}
.commentCont_write #regCommentTa {
  resize: none;
  border: 1px solid rgb(233, 236, 239);
  line-height: 1.75;
}
.commentCont_reg {
  display: flex;
  padding-bottom: 1.5rem;
}
#regCommentBtn {
  margin-left: auto; /* flex의 왼쪽정렬 */
}
.commentCont_list_profile {
  display: flex; /* 자식 div자측정렬 */
}
.commentCont_list> div{
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
  padding-left: 0.75rem;
}
.commentCont_profileInfo_date {
  font-size: 0.75rem;
  color: rgb(134, 142, 150);
}
.commentCont_list_content {
  padding: 1rem 0 2rem;
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
.commentCont_list_show, .commentCont_list_hide{
    position: relative;
    top: 2px;
}
.nestedComment_show{
    display: block;
}
.nestedComment_hidden{
    display: none;
}
.nestedCommentCont_background{
  border: 1px solid rgba(0, 0, 0, 0.02);
  background-color: rgba(0, 0, 0, 0.016);
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.3125rem;
}
.nestedCommentCont_hr{
  margin-bottom:1rem;
  border-bottom: 1px solid rgb(233, 236, 239);
}
.nestedCommentCont_profile {
  display: flex; /* 자식 div자측정렬,flex의 default가 행정렬 */
  padding-bottom:1.5rem;
}
.nestedCommentCont_comment{
  margin-bottom: 1.7rem;
}
#writeNestedCommentBtn{
  width: 100%;
}
.nestedCommentCont_write {
  margin-bottom: 20px;
}
.nestedCommentCont_write #regNewCommentTa {
  resize: none;
  border: 1px solid rgb(233, 236, 239);
  line-height: 1.75;
}
.nestedCommentCont_write_buttons{
  display: flex;
  justify-content: flex-end;
}
#writeNestedCommentCancelBtn{
  margin-right: 0.7rem;
}
</style>