// ES6 Modules or TypeScript
import Swal from "sweetalert2";

const successMessageList = {
    register: "登録しました。",
    update: "修正しました。",
    delete: "削除しました。",
};

const successMessage = (status = "register", msg) =>
    Swal.fire({
        title: successMessageList[status],
        text: msg,
        icon: "success",
        showConfirmButton: false,
        timer: 1500,
    });

const okMessage = (msg) =>
    Swal.fire({
        html: `<h2>${msg}</h2>`,
        icon: "success",
        showConfirmButton: false,
        timer: 1500,
    });

const confirmMessage = (msg) =>
    Swal.fire({
        title: "お知らせ",
        text: msg,
        showCancelButton: true,
        confirmButtonText: "確認",
    });
/**
 * #유저에러 400
 * 700번대 (경고창)
 * // 서버에가져온 메세지표시
 * // 페이지이동 없음
 *
 * 700번대이외 (에러창)
 * // 클라이언트 메세지표시함 (화면에서정의한메세지)
 * // 에러페이지 이동
 *
 * # 서버에러 500 (에러창)
 * // 클라이언트 메세지표시함 (화면에서정의한메세지)
 * // 에러페이지 이동
 */
const errorMessage = (err) => {
    const ERR_RESPONSE = err.response; // HTTP상태코드
    const ERR_STATUS = ERR_RESPONSE?.status; // HTTP상태코드

    // 400번 에러, 사용자 에러 처리
    if (ERR_STATUS >= 400 && ERR_STATUS < 500) {
        const ERR_INFO = ERR_RESPONSE.data; // 사용자정의 에러 정보
        const ERR_CODE = ERR_INFO.code; // 사용자정의 에러 코드

        // 서버에서 정의한 700 ~ 800번 사이의 사용자 정의 에러를 표시함
        if (ERR_CODE >= 700 && ERR_CODE < 800) {
            const ERR_MESSAGE = ERR_INFO.message; // 사용자정의 에러 메세지
            return warningMessage(ERR_MESSAGE); // 경고창에 서버에서 정의한 사용자 에러메세지를 표시
        } else {
            // 서버에 정의되어있지 않은 HTTP코드가 400번대의 에러
            return Swal.fire({
                title: "エラー",
                html: ERR_INFO.message,
                icon: "error",
                confirmButtonText: "確認",
            }).then(() => {
                location.href = "/NotFound";
            });
        }
    } else if (ERR_STATUS >= 500) {
        // 500번 에러, 서버에러
        const ERR_MESSAGE_500 =
            "予期しないサーバ内部エラーが発生しました。<br>しばらくしてからもう一度お試しください。";

        return Swal.fire({
            title: "エラー",
            html: ERR_MESSAGE_500,
            icon: "error",
            confirmButtonText: "確認",
        }).then(() => {
            location.href = "/NotFound";
        });
    } else {
        // 그외 화면등에서 발생하는 예기치 않은 에러..(CORS,타임아웃등)
        const ERR_MESSAGE_500 =
            "予期しないサーバ内部エラーが発生しました。<br>しばらくしてからもう一度お試しください。";

        return Swal.fire({
            title: "エラー",
            html: ERR_MESSAGE_500,
            icon: "error",
            confirmButtonText: "確認",
        }).then(() => {
            location.href = "/NotFound";
        });
    }
};

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
    infoMessage,
});
