import { initializeApp } from "firebase/app";
import {
    getAuth,
    setPersistence,
    browserSessionPersistence,
    onAuthStateChanged,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
} from "firebase/auth";
import store from "@/store";
//SDK v9를 사용, SDK8는 firebase를 통채로 사용했다고하면 SDK9는 필요한 모듈(auth)만 import하기때문에 적은 용량의 이점이 있음

// 파이어베이스 환경설정파일
const firebaseConfig = {
    apiKey: process.env.VUE_APP_KEY,
    authDomain: process.env.VUE_AUTH_DOMAIN,
    databaseURL: process.env.VUE_DATABASE_URL,
    projectId: process.env.VUE_PROJECT_ID,
};

export default {
    app: null,

    // 파이어베이스 초기화 부분
    init() {
        initializeApp(firebaseConfig); // firebase 초기화
        this.auth = getAuth(); // 인증정보모듈 (인증 서비스만 사용)
        setPersistence(this.auth, browserSessionPersistence); // 세션에 로그인정보저장(창닫으면 초기화)
    },

    // 이메일과 패스워드로 로그인한다
    // 파이어베이스인증결과, JWT Token이 돌아온다. JWT는 세션스토리지에 저장한다.
    signInWithEmailAndPassword(email, password) {
        return signInWithEmailAndPassword(this.auth, email, password).then(
            // 로그인성공시
            async (res) => {
                await res.user.getIdToken().then((idToken) => {
                    store.commit("onAuthEmailChanged", res.user.email); // 이메일 저장
                    store.commit("onUserStatusChanged", true); // 로그인 OK
                    sessionStorage.setItem("jwt", idToken); // 로그인 성공시 ID토큰을 세션스토리지에 저장
                });
                return "TODO로그인성공";
            },
            // 로그인실패시
            (err) => {
                store.commit("onAuthEmailChanged", ""); // 이메일 저장 삭제
                store.commit("onUserStatusChanged", false); // 로그인 NG
                sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
                if (
                    err.code == "auth/user-not-found" ||
                    err.code == "auth/wrong-password"
                ) {
                    throw new Error("TODO입력정보확인해주셈");
                } else {
                    throw new Error("TODO로그인실패");
                }
            }
        );
    },
    // 회원가입
    signUpWithEmailAndPassword(email, password) {
        createUserWithEmailAndPassword(this.auth, email, password)
            .then((res) => {
                //서버에 가입정보 넘김
                console.log(res);
                // router.push('/signin');
            })
            .catch((err) => {
                console.log(err.message);
            });
    },
    // 로그아웃
    // 로그아아웃을 성공하면 세션스토리지의 JWT를 삭제하고 vuex에 유저정보갱신기능을 실행해서 유저상태를 로그아웃으로 만든다
    logout() {
        return signOut(this.auth).then(() => {
          sessionStorage.removeItem("jwt") // ID토큰을 세션스토리지에 삭제
          store.commit("onAuthEmailChanged", ""); // 이메일 저장 삭제
          store.commit('onUserStatusChanged', false);  // 로그인 NG
          return 'TODO로그아웃성공'
        }).catch(() => {
          throw new Error('TODO로그아웃안됨')
        })
    },
    //로그인상태갱신,JWT의 상태갱신
    onAuth() {
        onAuthStateChanged(this.auth, async (user) => {
            // 갱신해온 정보에 유저정보가 있으면 JWT를 갱신하고 유저이메일, 정보를 저장한다
            if (user) {
                // 토큰을 세션에 설정
                await user.getIdToken()
                .then((idToken) => {
                  sessionStorage.setItem('jwt', idToken);
                })
                .catch(() => {
                  sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
                });

                store.commit("onAuthEmailChanged", user.email); // 이메일 저장
                if (user.uid) {
                    store.commit("onUserStatusChanged", true); // 로그인 OK
                } else {
                    store.commit("onUserStatusChanged", false); // 로그인 NG
                }
            } else {
                // 갱신해온 정보에 유저정보가 없다면 JWT와 기존유저정보를 지움
                store.commit("onAuthEmailChanged", "");
                store.commit("onUserStatusChanged", false);
            }
        });
    },
    // 초기 렌더링시 사용
    onAuthStateChanged
};
