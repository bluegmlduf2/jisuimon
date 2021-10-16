<template>
  <div class="postCont">
    <h1 class="postCont_title">제목</h1>
    <div class="postCont_writer"><b>작성자명</b>&nbsp;·&nbsp;날짜</div>
    <div class="postCont_ingredient">
      <span >재료1</span>
      <span>재료2</span>
      <span>재료3</span>
      <span>재료4</span>
    </div>
    <div class="postCont_index">
      <h3>김치찌게만들기 목록</h3>
      <ol v-if="listShow">
        <li>순서1</li>
        <li>순서2</li>
        <li>순서3</li>
        <li>순서4</li>
        <li>순서5</li>
      </ol>
      <div class="postCont_index_list" @click="listShow=!listShow">{{listShow?"▲ 숨기기":"▼ 목록보기"}} </div>
    </div>
    <div class="postCont_article">
      <p v-for="i in 4" :key="i">Ipsum"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
      "There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..."
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
      Fusce a libero vel enim congue volutpat. Fusce pulvinar maximus facilisis. 
      Proin vitae odio ac lectus eleifend eleifend ut sed nisl. Nunc vulputate finibus eros vitae bibendum. Vestibulum imperdiet luctus nisl ut pellentesque. 
      Suspendisse semper ante fermentum libero suscipit finibus. Curabitur non imperdiet tellus. 
      Mauris sed leo eget velit porttitor pulvinar ac quis ipsum. Vivamus tincidunt nunc sem, sit amet mattis felis malesuada ut.</p>
    </div> 
  </div>
</template>

<script>
export default {
    name:"Post",
    data() {
      return {
        listShow:false
      }
    },
}
</script>

<style>
.postCont{
  padding-bottom: 80px;

}
.postCont *{
  text-align: left;
  margin-bottom: 20px;
}

.postCont_title{
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 30px;
}
.postCont_writer{
  
}
.postCont_ingredient span{
  background: rgb(241, 243, 245);
  display: inline-flex;
  align-items: center;
  color: rgb(12, 166, 120);
  text-decoration: none;
  font-weight: 500;
  height: 1.5rem;
  font-size: 1rem;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

.postCont_index{
  padding: 1rem;
  margin-top: 2rem 0;
  background: rgb(242, 242, 242);
  border-radius: 8px;
  box-shadow: rgb(0 0 0 / 6%) 0px 0px 4px 0px;
  position: relative;
  color: rgb(33, 37, 41);
}
.postCont_index ol{
  font-size: 0.875rem;
  margin-bottom: -1rem;
  padding-left: 1.7rem;
}
.postCont_index_list{
  margin-top: 3rem;
  margin-bottom: 0px;
  cursor: pointer;
}
.postCont_article{
  line-height: 1.75; /* 폰트사이즈*1.75 */
}
@media (min-width: 577px){
  /* 현재 넓이가 577px이상 */
  .postCont{
    padding-top: 10vh;
  }
}
@media (min-width: 992px){
  /* 넓이가 992px 이상 여백추가*/
  .postCont{
    padding-left:160px;
    padding-right:160px;
  }
}

</style>