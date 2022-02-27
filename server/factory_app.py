'''
Flask설정
'''
from flask import Flask
from controller import post
from controller import food
from controller import comment
from controller import user
from flask_cors import CORS
import configparser#환경설정파일parser
import firebase_admin
from firebase_admin import credentials, auth

dict_confmode = {
    'test': 'setting.TestMode',
    'dev': 'setting.DevMode',
    'pro': 'setting.InitConf'
}

# Application Factories (it can have instances of the application with different settings)
def create_app(config_mode="test"):
    # Flask실행파일을 읽음
    app = Flask(__name__)
    # Flask의 환경설정 파알을 읽음
    confmode = dict_confmode[config_mode]
    app.config.from_object(confmode)#매개변수:경로와 파일의 클래스명

    #세션의암호키설정
    config = configparser.ConfigParser()
    config.read('{rootPath}/key.ini'.format(rootPath=app.root_path))
    app.secret_key= config['DEFAULT']['SESSION_KEY']
    
    # 파이어베이스 환경설정
    cred = credentials.Certificate('{rootPath}/yoon-firebase-adminsdk-p1v9u-b1bb4f62fd.json'.format(rootPath=app.root_path))
    app.firebase=firebase_admin.initialize_app(cred)
    app.auth=auth

    # 파일경로 설정
    app.userImgPath=app.root_path + "/static/userImg/" # 유저이미지 경로
    app.userDefaultImg=app.root_path+"/static/defaultImg/noUser.png" # 기본 유저이미지 경로
    app.fileTempPath = app.root_path+'/static/temp/' #　게시물이미지 임시파일위치
    app.fileDestPath = app.root_path+'/static/contentImg/' # 게시물이미지 저장용폴더위치
    app.fileDestDefaultPath = app.fileDestPath+'defaultImg/' # 게시물이미지 디폴트 저장용폴더위치
    app.urlTempPath = '/static/temp/' # 임시 파일위치 (url반환용)
    app.urlDestPath = '/static/contentImg/' # 이미지 파일위치 (url반환용)
    app.urlDestDefaultPath = '/static/contentImg/defaultImg/' # 타이틀 이미지 기본파일위치 (url반환용)
    
    # 개발모드일시 flask웹서버를 사용하기때문에 cors가 발생함 이를 방지하기 위해 아래의 cors설정추가
    # supports_credentials :사용자가 인증된 요청을 할수있게함(쿠키,세션)
    # CORS로 추가해야하는 URL의 확인은 크롬 디버깅툴에서 REQUEST실패한 헤더의 ORGIN을 넣어주면 헤당 ORIGIN은 요청을 허용한다는 의미가된다
    if config_mode == 'pro':
        CORS(app,resources={r'*': {'origins': "https://jisuimon.cf"}},supports_credentials=True)
    else:
        CORS(app,resources={r'*': {'origins': ['http://localhost:8080']}},supports_credentials=True)

    #매개변수로 bluePrint객체를 받는다. 그러나 import해서 해당 컨트롤러에 blueprint객체를 가져와서 사용
    HOME_URL = config['DEFAULT']['HOME_URL'] # home url (/jisuimon/)

    app.register_blueprint(post.post_controller, url_prefix=HOME_URL)
    app.register_blueprint(food.food_controller, url_prefix=HOME_URL)
    app.register_blueprint(user.user_controller, url_prefix=HOME_URL)
    app.register_blueprint(comment.comment_controller, url_prefix=HOME_URL)

    return app