<template>
  <div class="loginCont">
    <h1>Login</h1>
    <div id="firebaseui-auth-container"></div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import app from '@/firebase'; // fireBase초기화파일

export default {
  created() {
        const auth = getAuth(app);
        signInWithEmailAndPassword(auth, 'red@nate.com', '111111')
        .then((userCredential) => {
            console.log(1)
            // Signed in
            console.log(userCredential)
            const user = userCredential.user;
            // ...
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
        });
  },
};
</script>
