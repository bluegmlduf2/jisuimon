import { initializeApp } from "firebase/app";
import {
    getAuth,
    setPersistence,
    browserSessionPersistence,
    onAuthStateChanged,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    updateProfile,
    updatePassword,
    deleteUser,
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
        setPersistence(this.auth, browserSessionPersistence); // 세션에 로그인 정보저장(현재탭에만 적용,창닫으면 초기화)
        // setPersistence(this.auth, browserLocalPersistence); // 로컬스토리지에 로그인 정보저장(로그아웃하지않는한 지속,이게 디폴트임)
    },

    // 이메일과 패스워드로 로그인한다
    // 파이어베이스인증결과, JWT Token이 돌아온다. JWT는 세션스토리지에 저장한다.
    signInWithEmailAndPassword(email, password) {
        return signInWithEmailAndPassword(this.auth, email, password).then(
            // 로그인성공시
            () => "TODO로그인성공",
            // 로그인실패시
            (err) => {
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
        let current_user; // 파이어베이스 회원등록 유저
        return createUserWithEmailAndPassword(this.auth, email, password)
            .then(
                // 회원가입성공시 user를 반환한다
                (userCredential) => userCredential.user,
                // 회원가입실패시
                (err) => {
                    //TODO 실패시 서버의 uid삭제
                    if (err.code == "auth/email-already-in-use") {
                        throw new Error("TODO이미사용중인아이디임");
                    } else {
                        throw new Error("TODO회원등록실패");
                    }
                }
            )
            .then(async (user) => {
                current_user = user; // 서버에서 등록실패할 경우 파이어베이스의 유저삭제용
                const payload = { method: "post" };
                return await store.dispatch("signUp", payload);
            })
            .catch(async (err) => {
                // 에러메세지 정의
                const ERR_MESSAGE = err.response?.data.message
                    ? err.response.data.message // 서버에러메세지
                    : err.message; // 파이어베이스에러메세지
                // 유저등록중 서버 에러시 파이어베이스 유저삭제
                if (current_user) {
                    await deleteUser(current_user);
                }
                throw new Error("TODO 에러메세지.." + ERR_MESSAGE);
            })
            .then(() => "TODO회원등록성공");
    },
    // 로그아웃
    // 로그아아웃을 성공하면 세션스토리지의 JWT를 삭제하고 vuex에 유저정보갱신기능을 실행해서 유저상태를 로그아웃으로 만든다
    logout() {
        return signOut(this.auth)
            .then(() => {
                sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
                store.commit("onAuthEmailChanged", ""); // 이메일 저장 삭제
                store.commit("onUserStatusChanged", false); // 로그인 NG
                return "TODO로그아웃성공";
            })
            .catch(() => {
                throw new Error("TODO로그아웃안됨");
            });
    },
    // 유저정보갱신
    updateUser(updateInfo) {
        const USER_INFO = {};

        switch (updateInfo.flag) {
            case "profileImg":
                USER_INFO.photoURL = updateInfo.photoURL;
                break;
            case "nickName":
                USER_INFO.displayName = updateInfo.nickName;
                break;
        }
        return updateProfile(this.auth.currentUser, USER_INFO)
            .then(() => "TODO갱신성공")
            .catch(() => {
                throw new Error("TODO갱신실패");
            });
    },
    // 유저비밀번호갱신
    updatePass(updateInfo) {
        // TODO 현재패스워드 체크 후 문제없으면 갱신
        return updatePassword(this.auth.currentUser, updateInfo.newPassword)
            .then(() => {
                return "TODO비밀번호갱신성공";
                // Update successful.
            })
            .catch((error) => {
                // An error ocurred
                // ...
                throw new Error("TODO비밀번호갱신실패");
            });
    },
    //로그인상태갱신,JWT의 상태갱신
    onAuth() {
        onAuthStateChanged(this.auth, async (user) => {
            // 갱신해온 정보에 유저정보가 있으면 JWT를 갱신하고 유저이메일, 정보를 저장한다
            if (user?.uid) {
                const ID_TOKEN = await user.getIdToken(); // 토큰취득
                sessionStorage.setItem("jwt", ID_TOKEN); // 토큰을 세션에 저장
                store.commit("onAuthEmailChanged", user.email); // 이메일 저장
                store.commit("onUserStatusChanged", true); // 로그인 상태 OK 저장
            } else {
                // 갱신해온 정보에 유저정보가 없다면 JWT와 기존유저정보를 지움
                sessionStorage.removeItem("jwt"); // ID토큰을 세션스토리지에 삭제
                store.commit("onAuthEmailChanged", ""); // 저장된 이메일 비움
                store.commit("onUserStatusChanged", false); // 로그인 상태 NG 저장
            }
        });
    },
    // 초기 렌더링시 사용
    onAuthStateChanged,
};
