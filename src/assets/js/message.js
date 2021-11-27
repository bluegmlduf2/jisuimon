// ES6 Modules or TypeScript
import Swal from 'sweetalert2'

const successMessageList = {
    regist: "登録しました。",
    update: "修正しました。",
    delete: "削除しました。",
};

const successMessage = () =>
    Swal.fire({
        title: "Your work has been saved",
        text: successMessageList.regist,
        icon: "success",
        showConfirmButton: false,
        timer: 1500,
    });

const errorMessage = (err) =>
    Swal.fire({
        title: "エラー",
        text: err,
        icon: "error",
        confirmButtonText: "確認",
    }).then(()=>{
        location.href="/NotFound";
    });

const warningMessage = (msg) =>
    Swal.fire({
        title: "お知らせ",
        text: msg,
        icon: "warning",
        confirmButtonText: "閉じる",
    });

const infoMessage = (msg) =>
    Swal.fire({
        title: "お知らせ",
        text: msg,
        icon: "info",
        confirmButtonText: "閉じる",
    });

export default Object.freeze({
    successMessage,
    errorMessage,
    warningMessage,
    infoMessage
});
