import message from './message.js';

export default class UploadAdapter {
    constructor( loader ) {
        // The file loader instance to use during the upload.
        this.loader = loader;
    }

    // Starts the upload process.
    upload() {
        return this.loader.file
            .then( file => new Promise( ( resolve, reject ) => {
                this._initRequest();
                this._initListeners( resolve, reject, file );
                this._sendRequest( file );
            } ) )
    }

    // Aborts the upload process.
    abort() {
        if ( this.xhr ) {
            this.xhr.abort();
        }
    }

    // Initializes the XMLHttpRequest object using the URL passed to the constructor.
    _initRequest() {
        const rootUrl = process.env.VUE_APP_SERVER_URL; // env파일에 저장된 서버 Root_url
        const xhr = this.xhr = new XMLHttpRequest();
        xhr.open( 'POST', `${rootUrl}/imageUploadTemp`, true ); //xhr.open('POST', 'http://localhost:8000/api/image/upload', true); //imageUploadTemp
        xhr.responseType = 'json';
    }

    // Initializes XMLHttpRequest listeners.
    _initListeners( resolve, reject, file ) {
        const xhr = this.xhr;
        const loader = this.loader;
        const genericErrorText = `ファイルのアップロードができません ${ file.name }.`;

        xhr.addEventListener( 'error', () => reject( genericErrorText ) );
        xhr.addEventListener( 'abort', () => reject() );
        xhr.addEventListener( 'load', () => {
            const response = xhr.response; // 서버에서 전달받은 메세지

            if ( !response || response.error ) {
                return reject( response && response.error ? response.error.message : genericErrorText );
            }
            
            // 400번 에러, 사용자 에러 처리
            if (xhr.status >= 400 && xhr.status < 500) {
                message.warningMessage(response.message,'html')
                reject()
            }
            // 500번 에러, 서버에러
            if (xhr.status >= 500) {
                message.warningMessage(response.message)
                reject()
            }
            // 성공시에 메세지 표시
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve( {
                    default: response.url //업로드된 파일 주소
                } );
            }
        } );

        if ( xhr.upload ) {
            xhr.upload.addEventListener( 'progress', evt => {
                if ( evt.lengthComputable ) {
                    loader.uploadTotal = evt.total;
                    loader.uploaded = evt.loaded;
                }
            } );
        }
    }

    // Prepares the data and sends the request.
    _sendRequest( file ) {
        // Prepare the form data.
        const data = new FormData();
        // 입력한 데이터를 imageFile라는 파라메터명으로 넣어서 보낸다
        data.append( 'imageFile', file );

        // Send the request.
        this.xhr.send( data );
    }
}