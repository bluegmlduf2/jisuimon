// ES6 Modules or TypeScript
import Swal from 'sweetalert2'

const successMessageList = {
    regist: "登録しました。",
    update: "修正しました。",
    delete: "削除しました。",
};

const successMessage = (msg) =>
    Swal.fire({
        title: successMessageList.regist,
        text: msg,
        icon: "success",
        showConfirmButton: false,
        timer: 1500,
    })

const okMessage = (msg) =>
    Swal.fire({
        html: `<h2>${msg}</h2>`,
        icon: "success",
        showConfirmButton: false,
        timer: 1500,
    })

const confirmMessage = (msg) =>
    Swal.fire({
        title: 'お知らせ',
        text: msg,
        showCancelButton: true,
        confirmButtonText: '確認',
      })

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
    okMessage,
    confirmMessage,
    errorMessage,
    warningMessage,
    infoMessage
});
