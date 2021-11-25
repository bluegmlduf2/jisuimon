<template>
  <div class="writeCont">
    <div class="input-group mb-3">
      <input type="text" class="form-control" placeholder="タイトルを入力してください">
    </div>
    <div class="writeCont_materialList">
      <span v-for="(ingredient,i) in ingredientList" :key="i" @click="removeIngredient">{{ingredient.food_name}}</span>
    </div>
    <div class="writeCont_add_materialList mb-3">
      <div class="writeCont_add_materialList_select input-group input-group-sm">
        <input type="text" class="form-control" placeholder="食材を選んでください" @keyup="getFood" @change="selectFood" list="foodDataList">
        <datalist id="foodDataList">
          <option v-for="(food,i) in foodList" :key="i" >{{food['food_name']}}</option>
        </datalist>
      </div>
      <div class="writeCont_add_materialList_weight input-group input-group-sm ">
        <input type="number" class="form-control" placeholder="数量を入力してください" >
        <div class="input-group-append">
          <button id="selectUnitBtn" class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="false">単位</button>
          <div class="dropdown-menu dropdown-menu-right dropdown-menu-lg-left">
            <a class="dropdown-item" href="#">個</a>
            <a class="dropdown-item" href="#">ml</a>
            <a class="dropdown-item" href="#">大さじ</a>
            <a class="dropdown-item" href="#">小さじ</a>
            <div role="separator" class="dropdown-divider"></div>
            <div class="input-group input-group-sm">
              <input type="text" class="form-control" style="margin-left:5px" placeholder="直接入力" aria-label="" aria-describedby="writeUnitBtn">
              <div class="input-group-append" style="margin-right:5px">
                <button class="btn btn-light" type="button" id="writeUnitBtn">選択</button>
              </div>
            </div>
          </div>
        </div>
      </div>
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
      foodList:[], // 검색한 재료리스트
      ingredientList:[] // 추가한 재료리스트
    };
  },
  methods:{
    // 재료 검색 결과리스트 가져오기
    getFood(event) {
      const INPUT_FOOD=event.target.value // 입력한 재료
      // 2글자 이상부터 검색
      if(INPUT_FOOD.length<2){
        return
      }
      this.loading = true;
      const payload = {method: "get", food_name: INPUT_FOOD};
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
    // 선택한 재료 추가
    selectFood(event){
      const SELECTED_OPTION = event.target // 선택한 재료
      const DUPLICATION_FOOD = this.ingredientList.filter(e => e.food_name === SELECTED_OPTION.value).length // 이미 추가한 재료 여부
      // 이미 추가한 재료일 경우에 종료
      if(DUPLICATION_FOOD){
        this.$message.infoMessage("既に登録されている材料です。")
        return
      }
      const SELECTED_FOOD = this.foodList.find(e => e.food_name === SELECTED_OPTION.value) // 선택한 재료의 정보 가져오기
      
      // 초기화
      this.foodList=[]
      SELECTED_OPTION.value=""
      // 선택한 재료추가 
      this.ingredientList.push(SELECTED_FOOD)
    },
    // 재료삭제
    removeIngredient(event){
      const SELECTED_OPTION = event.target // 선택한 재료
      this.ingredientList = this.ingredientList.filter(e => e.food_name !== SELECTED_OPTION.textContent) // 재료 삭제
    },
    insertPost() {
      this.loading = true;
      const payload = {method: "post", postId: this.$route.params.postId};
      this.$store
        .dispatch("insertPost", payload)
        .then((result) => {
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
.writeCont_add_materialList{
  display: flex;
}
.writeCont_add_materialList_select{
  flex-grow: 3;
  flex-basis: 200px;
}
.writeCont_add_materialList_weight{
  margin-left: 5px;
  flex-grow: 1;
  flex-basis: 180px;
}
#selectUnitBtn{
  background-color: #fff;
  border:1px solid #ced4da;
  width: 80px;
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
#writeUnitBtn{
  background-color: #fff;
  border:1px solid #ced4da;
}
</style>