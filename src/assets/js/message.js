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
        title: "Error!",
        text: err,
        icon: "error",
        confirmButtonText: "Cool",
    });

export default Object.freeze({
    successMessage,
    errorMessage,
});
