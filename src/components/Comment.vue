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
        <div class="commentCont_list_profile">
          <div class="commentCont_list_profileImg">
            <img :src="`${comment.user_image}`" alt="profileImg">
          </div>
          <div class="commentCont_list_profileInfo">
            <div class="commentCont_list_profileInfo_name">
              <b>{{ comment.nickname }}</b>
            </div>
            <div class="commentCont_list_profileInfo_date">{{$moment(comment.comment_create_date).format("YYYY年 MM月 DD日 dddd  hh時 mm分")}}</div>
          </div>
        </div>
        <div class="commentCont_list_content">
          {{ comment.comment_content }}
        </div>
        <div class="commentCont_list_moreComment" >
          <span v-if="comment.showState" @click="comment.showState=!comment.showState" class="material-icons commentCont_list_show">remove_circle_outline</span>
          <span v-if="!comment.showState" @click="comment.showState=!comment.showState" class="material-icons commentCont_list_hide">add_circle_outline</span>
          <span @click="comment.showState=!comment.showState">&nbsp;{{comment.comment_reply.length>0?`${comment.comment_reply.length}件のコメント`:"コメントを残す"}}</span>
          <!-- nestedComment 대댓글 -->
          <div class="nestedCommentCont" :class="{'nestedComment_show': comment.showState,'nestedComment_hidden': !comment.showState }">
              <div v-for="commentReply in comment.comment_reply" :key="commentReply.commont_reply_id">&emsp;{{commentReply.comment_reply_content}}</div>
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
    comment: Array,
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
}
#regCommentBtn {
  margin-left: auto; /* flex의 왼쪽정렬 */
  background: rgb(18, 184, 134);
}
.commentCont_list_profile {
  display: flex; /* 자식 div자측정렬 */
  padding-top: 1.5rem;
}
.commentCont_list > div:not(:first-of-type) {
  border-top: 1px solid rgb(233, 236, 239);
}
.commentCont_list_profileImg > img {
  height: 2.5rem;
  widows: 2.5rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}
.commentCont_list_profileInfo {
  padding-left: 0.75rem;
}
.commentCont_list_profileInfo_date {
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
</style>