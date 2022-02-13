from flask import Blueprint, request, current_app, jsonify, send_from_directory,Markup
import time
import traceback
import simplejson as json  # dumps(객체) ->json문자열 , loads(json문자열) ->객체
import base64
from database import Connection
from functools import wraps
from jinja2 import utils # xssFilter
import re # 특정 문자열 사이 문자열 찾기 (정규식)
import shutil # 파일 이동용
import os # 파일 이동용
import random # 디폴트 이미지명 난수생성
import uuid # PK작성을 위한 UUID 생성
from PIL import Image  # 이미지 사이즈 변경
import datetime  # 이미지 업로드에서 사용할 시간모듈
import copy # 딕셔너리 객체복사용
from io import BytesIO # 저장용 버퍼객체
import inspect # 호출한 메서드의 이름 가져오기

'''
 아래는 예외처리에 관련된 공통항목이다
 exception_handler
 getMessage
 UserError
'''

# 예외처리 데코레이터
def exception_handler(func):
    @wraps(func)  # func.doc 과 같은 값을 잃어버리지 않도록 설정
    def inner_func():
        try:
            print("##### 메소드 시작 => ("+func.__name__+")#####")
            start = time.time()

            result = func()  # 인자로 전달받은 func 호출 / result는 func()의 반환값

            end = time.time()
            print("##### 메소드 종료 #####")
            print("소요시간: %5f" % (end-start))
        except UserError as e:
            # 사용자에러 처리
            return jsonify(e.errorInfo), 400
        except Exception as e:
            # 기타 예외 처리
            traceback.print_exc()
            return jsonify(getMessage(801)), 500
        else:
            # 성공적으로 반환된 값 전달
            return result
    return inner_func

# 유저 토큰 확인 데코레이터 (토큰이 필수값)
def check_token(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        # 토큰이 존재하지않으면 400번에러
        if not request.headers.get('authorization'):
            return jsonify(getMessage(705)), 400
        try:
            #user변수에 파이어베이스 유저정보 넣음
            user = current_app.auth.verify_id_token(request.headers['authorization'].replace("Bearer ",""))
            request.user = user
        except:
            #유효하지않은 토큰
            return jsonify(getMessage(705)), 400
        return func(*args, **kwargs)
    return wrap

# 유저 토큰 확인 데코레이터 (토큰이 선택값)
def get_token(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        try:
            user = None
            #유저 정보가 존재할 경우에 user변수에 파이어베이스 유저정보 넣음
            if request.headers.get('authorization'):
                user = current_app.auth.verify_id_token(request.headers['authorization'].replace("Bearer ",""))
            request.args.user = user # request.args가 변경불가능한 딕셔너리이기때문에 여기서 추가해준다 (ImmutableMultiDict)
        except:
            #유효하지않은 토큰
            return jsonify(getMessage(705)), 400
        return func(*args, **kwargs)
    return wrap

# d 맵핑된 메세지 반환
def getMessage(code, param=None):
    MESSAGE = {
        # 성공
        601: "成功しました",
        # 실패 (사용자)
        701: f"{param}を入力してください",
        702: "ファイル名が存在しません。\nファイルアップロード失敗しました",
        703: "空きファイルです。\nファイルアップロード失敗しました",
        704: "既に登録されているユーザーです",
        705: "",
        706: "ユーザー削除処理失敗しました",
        707: f"他のユーザーから登録された{param}が存在しますので削除できませんでした",
        # 실패 (서버)
        801: "予期しないエラーが発生しました。<br>しばらくしてからもう一度お試しください。",
        802: "ユーザー権限を確認してください",
        803: "存在しない投稿です"
    }
    return {
        "code": code,
        "message": MESSAGE[code]
    }

# 유저에러_Exception상속
class UserError(Exception):
    # 인스턴스 생성시 리턴되는 인스턴스변수
    def __init__(self, errCode, param=None):
        self.errorInfo = getMessage(errCode, param)

    # 객체가 print함수에 호출될때 표시되는 함수
    def __str__(self):
        return self.errorInfo['message']

'''
 아래는 이미지와 경로에 관련된 공통항목이다
 imageConfig
 imageParser
 imageFromContent
 getTitleImage
 getUserImage
 getUrlPath
 moveImageTempToDest
 deleteContentImage
'''
# 이미지 함수에 필요한 설정부분
def imageConfig():
    # 파일 이동에 필요한 설정부분
    fileTempPath = current_app.fileTempPath  # 　임시파일위치
    fileDestPath = current_app.fileDestPath # 저장용폴더위치
    imageTempForder = os.listdir(fileTempPath) # 임시파일이 위치한 폴더
    imageSaveForder = os.listdir(fileDestPath) # 저장용파일이 위치한 폴더

    return imageTempForder, imageSaveForder, fileTempPath, fileDestPath 

# 이미지파일을 base64형식변환 (섬네일사이즈)
def imageParser(src):
    # 이미지파일->이미지파일사이즈변경->버퍼메모리저장->base64인코딩
    image = Image.open(src)
    buffered = BytesIO()  # 버퍼(임시메모리) 객체생성
    # 이미지파일을 리사이즈 후 임시 메모리 객체 버퍼에 저장
    image.resize((24, 24)).save(buffered, format="JPEG")
    # 섬네일 이미지 반환 (버퍼의 내용을 base64형식으로 변환후 반환)
    return "data:image/jpeg;base64, " + \
        base64.b64encode(buffered.getvalue()).decode('utf-8')

# 게시글에서 이미지 추출
def imageFromContent(content):
    # 글에서 파일명 추출 temp -> contentImg
    removeStringBetween=re.findall(r'/static/contentImg/.+?&#34',content) # 특정 문자열 사이의 단어를 반환
    removeStringPath=[x.replace('/static/contentImg/','') for x in removeStringBetween] # 문자열의 패스제거
    return [x.replace('&#34','') for x in removeStringPath] # 문자열의 불필요한 뒷부분 제거후 최종파일명
    
# 게시글의 타이틀 이미지 경로 추출
def getTitleImage(data):
    titleImage=data['title_image'] # 타이틀이미지
    defaultFileNum=str((data['create_date'].second % 8)+1) # 게시물 작성시간 초를 기준으로 1-8정수획득
    if titleImage:
        # 유저 저장 타이틀 이미지
        return getUrlPath()+current_app.urlDestPath+titleImage # 타이틀 이미지 , 없을 경우에 기본 타이틀이미지 1~8중 임의선택 
    else:
        # 기본 타이틀 이미지, 없을 경우에 기본 타이틀이미지 1~8중 임의선택 
        return getUrlPath()+current_app.urlDestDefaultPath+'titleImage_'+defaultFileNum+'.jpg'

# 유저 이미지 경로 추출
def getUserImage(userImage):
    if userImage:
        # 유저 저장 이미지
        return current_app.userImgPath+userImage
    else:
        # 유저 기본 이미지
        return current_app.userDefaultImg

# 현재의 url 정보를 반환
def getUrlPath():
    url = request.host_url  # 홈 URL
    
    # 개발환경용 url 설정
    if current_app.env == 'development':
        url = "http://localhost:5000"
    
    return url

# 임시이미지 파일을 저장용 폴더에 이동
def moveImageTempToDest(imageFileNames):
    imageTempForder, imageSaveForder, fileTempPath, fileDestPath  = imageConfig() # 이미지 설정부분
    # 파일 이동 실행 부분
    for imageFile in imageTempForder:
        if imageFile in imageFileNames:
            shutil.move(fileTempPath + imageFile, fileDestPath + imageFile) # 파일이동

# 저장용 폴더의 이미지 파일을 삭제
def deleteContentImage(imageFileNames):
    imageTempForder, imageSaveForder, fileTempPath, fileDestPath  = imageConfig() # 이미지 설정부분
    # 파일 삭제 부분
    for imageFile in imageSaveForder:
        if imageFile in imageFileNames:
            imagefileWithFullPath=fileDestPath + imageFile # 저장용 이미지 파일
            # 파일이 존재할 경우 삭제
            if os.path.isfile(imagefileWithFullPath):
                os.remove(imagefileWithFullPath) # 파일삭제

'''
 아래는 보안에 관련된 공통항목이다
 xssFilter
 htmlUnescape
'''
# jinja를 이용한 xss필터함수
def xssFilter(args):
    escapedHTML=str(utils.escape(args))
    # script태그를 막기위해 설정(일부만 막을수있음..)
    escapedHTML=escapedHTML.replace("script", "")
    return escapedHTML

# escape된 HTML을 다시 HTML형식으로 변환
def htmlUnescape(args):
    return Markup(args).unescape()

'''
 아래는 유일키 생성 항목이다
 getUUID
'''
# UUID 추출 (36글자)
def getUUID():
    return str(uuid.uuid4()) # 랜덤 uuid반환

'''
 아래는 파이어베이스 유저 관련 항목이다
 getUser
 getUserAuth
'''
# 파이어베이스 유저정보 취득
def getUser(uid):
     # 파이어베이스 유저정보
    userInfo={
        'nickname':'脱退したユーザー',
        'user_image':None
    }

    # uid확인
    if uid:
        user = current_app.auth.get_user(uid) # 유저정보취득 (파이어베이스)

        # 유저 닉네임 (닉네임 존재하지않을시 생성타임스탬프를 이용해 유저닉네임생성) 삼항연산자
        nickname=not user.display_name and "USER" + str(user.user_metadata.creation_timestamp) or user.display_name
        
        #유저 프로필 이미지
        user_image=str(user.photo_url or '').replace(
            'http://', '') # None을 공백 문자열로 변환후 url을 공백 변환
        
        # 전달할 유저값
        userInfo['nickname']=nickname
        userInfo['user_image']=user_image

    return userInfo

# 유저 권한 정보 취득
def getUserAuth(login_uid,uid):
    auth = False # 게시물의 유저 권한
    if login_uid:
        # 로그인 유저와 데이터의 uid가 동일한 경우 데이터 관리 유저권한을 반환한다
        auth = True if login_uid['uid'] == uid else False

    return auth