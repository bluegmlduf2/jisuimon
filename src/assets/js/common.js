export default {
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
    },
};
