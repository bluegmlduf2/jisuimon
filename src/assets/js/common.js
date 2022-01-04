export default {
    data() {
        return {
            rootUrl : process.env.VUE_APP_SERVER_URL // env파일에 저장된 서버 Root_url
        }
    },
    // 라이플사이클일 경우 mixin먼저 호출
    // 컴포넌트 메서드가 우선권있음
    methods: {
        // HTML태그제거
        removeHtml(str) {
            str = str.replace(/<br\/>/gi, "\n");
            str = str.replace(/<(\/)?([a-zA-Z]*)(\s[a-zA-Z]*=[^>]*)?(\s)*(\/)?>/gi,"");
            str = str.replace(/(<([^>]+)>)/gi, "");
            str = str.replace(/&nbsp;/gi, "");
            return str;
        },
        // 숫자만 허용,공백허용안함
        allowNumber(str) {
            const REGEX = /[^0-9]/g; // 정규식, [^0-9] 숫자허용안함, ^[0-9] 숫자만 허용
            str=str.replace(REGEX, "") // 문자열에서 숫자가 아닌 모든 문자열을 빈 문자로 변경
            str=Number(str) // 가장 문자열의 가장 앞의 0을 지움
            return str;
        },
        // 이메일 양식체크
        checkEmail(str) {
            const REGEX = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i
            const isEmail= str.match(REGEX) != null ? true : false ;
            return isEmail;
        },
        // 비밀번호 양식체크 (최소 8글자,문자하나,숫자하나,특문하나)
        checkPass(str) {
            const REGEX = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/
            const isPass= REGEX.test(str) ? true : false ;
            return isPass;
        }
    },
};
