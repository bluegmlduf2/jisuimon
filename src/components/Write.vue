<template>
  <div class="writeCont">
    <div class="input-group mb-3">
      <input type="text" class="form-control" placeholder="タイトルを入力してください" v-model="formData.title">
    </div>
    <div class="writeCont_materialList">
        <span class="" v-for="(ingredient,i) in formData.ingredientList" :key="i" @click="removeIngredient(ingredient)" @mouseover="ingredient.showCancelFlg = true" @mouseleave="ingredient.showCancelFlg = false">
          {{`${ingredient.food_name}&emsp;/&nbsp;${ingredient.food_amt}${ingredient.food_unit}&emsp;${ingredient.showCancelFlg?"✖️":""}`}}
        </span>
    </div>
    <div class="writeCont_add_materialList mb-3 row">
      <div class="writeCont_add_materialList_select input-group input-group-sm col-md-7">
        <input type="text" class="form-control" placeholder="食材を選んでください" style="ime-mode: disabled" ref="foodInput" @keyup="getFood" @change="selectFood" list="foodDataList" :disabled="selectedFood.food_clicked">
        <button class="btn btn-sm bg-transparent material-icons" type="button" @click="clearFood" v-if="selectedFood.food_clicked">clear</button>
        <datalist id="foodDataList">
          <option v-for="(food,i) in foodList" :key="i" >{{food['food_name']}}</option>
        </datalist>
      </div>
      <div class="writeCont_add_materialList_input input-group input-group-sm col-md-4">
        <input type="number" class="form-control" ref="foodAmout" @input="inputAmout" min="1" placeholder="数量を入力してください" >
        <div class="input-group-append">
          <button id="selectUnitBtn" class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="false">{{selectedFood.food_unit?selectedFood.food_unit:"単位"}}</button>
          <div class="dropdown-menu dropdown-menu-right dropdown-menu-lg-left">
            <a class="dropdown-item" href="#" @click="selectUnit">個</a>
            <a class="dropdown-item" href="#" @click="selectUnit">ml</a>
            <a class="dropdown-item" href="#" @click="selectUnit">大さじ</a>
            <a class="dropdown-item" href="#" @click="selectUnit">小さじ</a>
            <div role="separator" class="dropdown-divider"></div>
            <div class="input-group input-group-sm">
              <input type="text" class="form-control" style="margin-left:5px" placeholder="直接入力" ref="foodUnit">
              <div class="input-group-append" style="margin-right:5px">
                <button class="btn btn-light" type="button" id="writeUnitBtn" @click="selectUnit">選択</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="input-group-append input-group-sm col-md-1">
        <button id="writeNestedCommentBtn" type="button" class="btn btn-sm btn-outline-success confirm_white_btn" @click="addIngredient"><b>追加</b></button>
      </div>
    </div>
    <ckeditor id="writeCont_content" :editor="editor" v-model="formData.content" :config="editorConfig" tag-name="textarea"/>
    <div class="writeCont_buttons">
      <div id="writeCont_back" @click="$router.go(-1)">
        <span class="material-icons">
          arrow_back
        </span>
      </div>
      <div class="writeCont_write">
        <button class="btn btn-success confirm_btn" id="writeContPostBtn" @click="registerPost">
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
import UploadAdapter from '@/assets/js/uploadAdapter.js'; // 이미지 업로드 어댑터
import common from '@/assets/js/common.js';

export default {
  name: "Write",
  components: {
    ckeditor: CKEditor.component,
  },
  mixins:[common],
  data() {
    return {
      editor: ClassicEditor,
      editorConfig:{
        toolbar: [ 'heading', '|', 'bold', 'italic', 'link', '|', 'imageUpload', '|', 'bulletedList', 'numberedList', '|', 'undo', 'redo' ],
        placeholder:"あなたの料理の作り方を教えてください", // ckEditor의 플레이스홀더
        extraPlugins: [this.uploader], // ckEditor에 이미지업로드 플러그인 추가
        language: 'ja',
      },// Ckeditor 설정 ClassicEditor.create(Ele,{여기에 들어갈 내용을 editorConfig안에 넣음}) 
      foodList:[], // 검색한 재료리스트
      selectedFood: { // 선택중인 재료
        food_id: null, //음식 ID
        food_name: null, //음식 이름
        food_amt: null, //음식 수량
        food_unit: null, // 음식 단위
        food_clicked: false, // 음식이 선택된지 여부
      },
      formData:{ // 서버에 전송할 데이터
        title:"", // 글제목
        content:"", // 글내용
        ingredientList:[], // 추가한 재료
      }
    };
  },
  methods:{
    // 이미지 업로더 어뎁터
    uploader(editor){
        editor.plugins.get( 'FileRepository' ).createUploadAdapter = ( loader ) => {
            return new UploadAdapter( loader );
        };
    },
    // 재료 검색 결과리스트 가져오기
    getFood(event) {
      const INPUT_FOOD=event.target.value // 입력한 재료
      // 2글자 이상부터 검색
      if(INPUT_FOOD.length<2){
        return
      }
      this.loading = true;
      const payload = {
        method: "get", 
        sendData: {food_name: INPUT_FOOD}
      };
      this.$store
        .dispatch("food",payload)
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
      const CLICKED_OPTION = event.target // 선택한 재료
      const DUPLICATION_FOOD = this.formData.ingredientList.filter(e => e.food_name === CLICKED_OPTION.value).length // 이미 추가한 재료 여부
      const SELECTED_FOOD = this.foodList.find(e => e.food_name === CLICKED_OPTION.value) // 선택한 재료의 정보 가져오기

      // 음식목록에서 선택한것이 아닌 일반 입력은 막기
      if(!SELECTED_FOOD){
        return
      }
      
      // 이미 추가한 재료일 경우에 종료
      if(DUPLICATION_FOOD){
        this.$message.infoMessage("既に登録されている材料です。")
        this.clearFood()
        return
      }

      SELECTED_FOOD.food_clicked=true // 선택중인 재료 입력창 입력금지 처리

      // 선택중인 재료 임시로 넣기
      Object.assign(this.selectedFood,SELECTED_FOOD)
    },
    // 선택중인 재료정보 삭제
    clearFood(){
      this.selectedFood.food_id=null
      this.selectedFood.food_name=null
      this.selectedFood.food_clicked=false
      this.foodList=[]
      this.$refs.foodInput.value=null
    },
    // 재료삭제
    removeIngredient(ingredient){
      // filter를 사용해서 food_name이 일치하지 않는것만 남긴다
      this.formData.ingredientList = this.formData.ingredientList.filter(e => e.food_name !== ingredient.food_name) // 재료 삭제
    },
    // 수량 입력
    inputAmout(event){
      const FOOD_AMT=event.target.value

      // 수학기호를 허용하지않음 ['e', '-', '+', '.']
      if(isNaN(Number(event.data))&&event.data){
        event.target.value=this.selectedFood.food_amt
        return
      }

      //정규식으로 입력된 문자열을 숫자만 허용,공백삭제
      const FOOD_AMT_REGEX=this.allowNumber(FOOD_AMT)
      // 수량입력
      this.selectedFood.food_amt=FOOD_AMT_REGEX;
    },
    // 단위 입력
    selectUnit(event){
      const ELEMENT_TYPE=event.target.type // 이벤트 발생 요소의 속성

      // 속성이 button인경우 단위 직접입력, 그외에 지정단위 선택
      if(ELEMENT_TYPE==="button"){
        this.selectedFood.food_unit=this.$refs.foodUnit.value // 단위명 추가
      }else{
        this.selectedFood.food_unit=event.target.outerText // 단위명 추가
      }
    },
    // 선택한 재료 추가
    addIngredient(){
      // some함수, 배열의 결과 값이 1개라도 참일때 참을 반환함 ,true감정
      // every함수, 배열의 결과 값이 1개라도 거짓일때 거짓을 반환함 ,false감정
      // 추가한 재료의 객체에 값이 하나라도 비어있는 경우에는 false를 반환한다. 
      const IS_EMPTY_FOOD=!Object.values(this.selectedFood).every(v=>v)
      // 선택중인 재료의 입력정보가 부족할 경우 경고
      
      if(IS_EMPTY_FOOD){
        this.$message.warningMessage("材料 / 数量 / 単位を選んでください");
        return
      }

      // 선택한 재료추가 
      this.selectedFood.showCancelFlg=false // 추가된 음식의 삭제 아이콘 표시 여부
      this.formData.ingredientList.push(this.selectedFood) // 선택한 재료 추가

      // 초기화
      this.foodList=[]
      this.$refs.foodInput.value=null
      this.$refs.foodAmout.value=""
      this.$refs.foodUnit.value=null
      this.selectedFood={        
        food_id: null,
        food_name: null,
        food_amt: null, 
        food_unit: null,
        food_clicked: false
      }
    },
    // 게시글 등록
    registerPost() {
      this.loading = true;

      // 입력값의 유효성체크
      if(this.validation())return
      
      const payload = { 
        method: "post",
        sendData: {}
      };

      payload.sendData=this.formData // 입력정보를 서버전송데이터에 넣음
      
      this.$store
        .dispatch("post", payload)
        .then((result) => {
          this.$message.successMessage()
          this.$router.push('/');
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
    // 입력값의 유효값 체크
    validation(){
      const TITLE = this.formData.title // 제목
      const CONTENT = this.formData.content // 글내용
      const INGREDIENT_LIST = this.formData.ingredientList // 재료

      // 제목 필수값체크
      if (!TITLE) {
        this.$message.warningMessage("タイトルを入力してください");
        return true
      }

      // 내용 필수값체크
      if (INGREDIENT_LIST.length === 0) {
        this.$message.warningMessage("材料を追加してください");
        return true
      }

      // 내용 필수값체크
      if (!CONTENT) {
        this.$message.warningMessage("作り方を入力してください");
        return true
      }

      return false
    }
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
  /* font-size: 1rem; */
  border-radius: 0.75rem;
  padding: 1rem;
  margin-right: 0.5rem;
  margin-bottom: 0.2rem;
}
.writeCont_materialList span:hover{
  background: rgb(245, 245, 245);
}
/* 넓이가 767px 이하가 될 경우, 마진을 준다. 
 부트스트랩의 col-md의 그리드 효과는 768px~ 부터 지속되므로
 767px에서 그리드 효과(12개칼럼)가 사라진다*/
@media (max-width: 767px) {
  .writeCont_add_materialList_select, .writeCont_add_materialList_input{
    margin-bottom: 1rem;
  }
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