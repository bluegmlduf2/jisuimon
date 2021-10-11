import { createStore } from 'vuex'

const store = createStore({
// 데이터 저장하는곳 , $store.state
  state(){
    return {
      like:0,
      selectedLike:false,
      moreDataVuex:null
    }
  },
// 데이터 변경하는곳 (디버깅등을 염두해서 데이터 변경을 한곳에서 처리) , $store.commoit()
  mutations:{
    addLike(state){
        state.like++;
        state.selectedLike=true;
    },
    removeLike(state){
        state.like--;
        state.selectedLike=false;
    },
    //vuex action 테스트용, 두번째 인자는 전달받는값
    showMoreVuex(state,data){
      state.moreDataVuex=data;
      console.log(state.moreDataVuex);
    }
  },
  // Ajax데이터 요청등을 처리 , $store.dispatch()
  actions : { 
    //context = 
    showMoreVuex(context){
      this.axios.get("https://codingapple1.github.io/vue/more1.json").then((result)=>{
        context.commit('showMoreVuex',result.data);
      })
    }
  }
})

export default store