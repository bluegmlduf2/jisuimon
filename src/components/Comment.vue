<template>
  <div class="commentCont">
    <h4>{{ comment.length }}件のコメント</h4>
    <div class="commentCont_write">
      <textarea
        class="form-control"
        id="regCommentTa"
        placeholder="コメントを残してください"
        rows="3"
      />
    </div>
    <div class="commentCont_reg">
      <button class="btn btn-success" id="regCommentBtn">
        <b>コメントを作成する</b>
      </button>
    </div>
    <!-- commentList -->
    <div class="commentCont_list">
      <div v-for="(comment) in comment" :key="comment.comment_id">
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
        <!-- 댓글 코멘ㅌ -->
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
                <div v-for="commentReply in comment.comment_reply" :key="commentReply.commont_reply_id">
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
                  <!-- 대댓글 글쓰기버튼 -->
                  <div class="nestedCommentCont_buttons"></div>
                </div>
                <div class="nestedCommentCont_newcomment">
                  <button id="writeNestedCommentBtn" type="button" class="btn btn-outline-success">コメント作成</button>
                </div>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import postsComments from "@/assets/js/postsComments.js";

export default {
  name: "Comment",
  props: {
    comment: Object,
  },
  data() {
    return {
      postsComments: postsComments,
    };
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
  background: rgb(18, 184, 134);
}
.commentCont_list_profile {
  display: flex; /* 자식 div자측정렬 */
}
.commentCont_list > div:not(:first-of-type) {
  border-top: 1px solid rgb(233, 236, 239);
}
.commentCont_profileImg > img {
  height: 2.5rem;
  widows: 2.5rem;
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
.nestedCommentCont_profile {
  display: flex; /* 자식 div자측정렬,flex의 default가 행정렬 */
  padding-bottom:1.5rem;
}
.nestedCommentCont_comment{
  margin-bottom: 1.8rem;
}
#writeNestedCommentBtn{
  width: 100%;
  color: rgb(18, 184, 134);
  border-color:rgb(18, 184, 134);
  background: rgb(255, 255, 255);
}

#writeNestedCommentBtn:hover , #writeNestedCommentBtn:active{
  color: rgb(255, 255, 255);
  background: rgb(18, 184, 134);
}
</style>