<template>
  <div class="writeCont">
    <div class="input-group mb-3">
      <input type="text" class="form-control" placeholder="タイトルを入力してください">
    </div>
    <div class="writeCont_materialList">
      <span v-for="(ingredient,i) in ingredientList" :key="i" @click="removeIngredient">{{ingredient.food_name}}</span>
    </div>
    <div class="input-group input-group-sm mb-3">
      <input type="text" class="form-control" placeholder="食材を選んでください" @keyup="getFood" @change="selectFood" list="foodDataList">
        <datalist id="foodDataList">
          <option v-for="(food,i) in foodList" :key="i" >{{food['food_name']}}</option>
        </datalist>
    </div>
    <ckeditor id="writeCont_content" :editor="editor" v-model="editorData" :config="editorConfig" tag-name="textarea"/>
    <div class="writeCont_buttons">
      <div id="writeCont_back" @click="$router.go(-1)">
        <span class="material-icons">
          arrow_back
        </span>
      </div>
      <div class="writeCont_write">
        <button class="btn btn-success confirm_btn" id="writeContPostBtn" @click="insertPost">
          <b>投稿する</b>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import CKEditor from "@ckeditor/ckeditor5-vue";
import '@ckeditor/ckeditor5-build-classic/build/translations/ja';// 일본어

export default {
  name: "Write",
  components: {
    ckeditor: CKEditor.component,
  },
  data() {
    return {
      editor: ClassicEditor,
      editorConfig:{
        language: 'ja',
      },
      editorData:"", // 글내용
      foodList:[], // 검색한 음식리스트
      ingredientList:[] // 재료리스트
    };
  },
  methods:{
    // 음식 검색 결과리스트 가져오기
    getFood(event) {
      const INPUT_FOOD_NAME=event.target.value
      this.loading = true;
      const payload = {method: "get", food_name: INPUT_FOOD_NAME};
      this.$store
        .dispatch("food", payload)
        .then((result) => {
          this.foodList=result.data
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    // 음식 선택시 추가
    selectFood(event){
      const SELECTED_OPTION = event.target // 선택한 옵션
      const SELECTED_FOOD = this.foodList.find(e => e.food_name === SELECTED_OPTION.value) // 음식추가
      // 초기화
      this.foodList=[]
      SELECTED_OPTION.value=""
      // 재료추가 
      this.ingredientList.push(SELECTED_FOOD)
    },
    // 재료삭제
    removeIngredient(event){
      const SELECTED_OPTION = event.target // 선택한 옵션
      this.ingredientList = this.ingredientList.filter(e => e.food_name !== SELECTED_OPTION.textContent) // 재료삭제
    },
    insertPost() {
      this.loading = true;
      const payload = {method: "post", postId: this.$route.params.postId};
      this.$store
        .dispatch("insertPost", payload)
        .then((result) => {
          console.log(result)
          this.posts = result.data[0]; //게시물 상세정보
          this.comment = result.data[1]; //게시물 댓글정보
          this.ingredient = result.data[2]; //게시물 재료정보
        })
        .catch((err) => {
          this.$message.errorMessage(err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  }
};
</script>
<style>
@media (min-width: 577px) {
  /* 현재 넓이가 577px이상 */
  .writeCont {
    padding-top: 10vh;
  }
}
.writeCont_materialList{
  margin-bottom: 10px;
  text-align: left;/* 자식요소가 inline-flex */
}
.writeCont_materialList span{
  background: rgb(241, 243, 245);
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  color: rgb(12, 166, 120);
  text-decoration: none;
  font-weight: 500;
  height: 1.5rem;
  font-size: 1rem;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-right: 0.5rem;
  margin-bottom: 0.2rem;
}
.writeCont_materialList span:hover{
  background: rgb(245, 245, 245);
}
.ck-content{
  height: 400px;
}
.writeCont_buttons{
  display: flex;
  justify-content: space-between; /** 요소가 일정한 간격을 두고 떨어짐, 2개 요소가 좌우로 최대한 멀어짐 */
  margin-top: 20px;
}
#writeCont_back{
  margin-left: 20px;
  cursor: pointer;
  padding:10px
}
#writeContPostBtn{
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
</style>