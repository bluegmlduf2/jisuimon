import { initializeApp } from "firebase/app";
//SDK v9를 사용, SDK8는 firebase를 통채로 사용했다고하면 SDK9는 필요한 모듈만 import하기때문에 적은 용량의 이점이 있음

// firebase 환경설정파일
const firebaseConfig = {
    apiKey: "<<apiKey>>",
    authDomain: "<<projectId>>.firebaseapp.com",
    databaseURL: "<<projectId>>.firebaseio.com",
    projectId: "<<projectId>>",
  };

// firebase 초기화  
const app=initializeApp(firebaseConfig);

export default app