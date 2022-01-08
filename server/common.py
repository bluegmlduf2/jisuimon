from flask import Blueprint, request, current_app, jsonify, send_from_directory
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
import copy

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

# 유저 토큰 확인 데코레이터
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
        705: "ユーザー権限を確認してください",
        706: "ユーザー削除処理失敗しました",
        # 실패 (서버)
        801: "システムエラー"
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
 아래는 이미지에 관련된 공통항목이다
 imageConfig
 imageParser
 imageFromContent
 getTitleImage
 moveImageTempToDest
'''
# 이미지 함수에 필요한 설정부분
def imageConfig():
    # 파일 이동에 필요한 설정부분
    fileTempPath = current_app.fileTempPath  # 　임시파일위치
    fileDestPath = current_app.fileDestPath # 저장용폴더위치
    imageForder = os.listdir(fileTempPath) # 임시파일이 위치한 폴더

    return imageForder, fileTempPath, fileDestPath 

# 이미지파일을 base64형식변환
def imageParser(src):
    with open(src, "rb") as image_file:
        # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
        return "data:image/jpeg;base64, " + \
            base64.b64encode(image_file.read()).decode('utf-8')

# 게시글에서 이미지 추출
def imageFromContent(content):
    # 글에서 파일명 추출 temp -> contentImg
    removeStringBetween=re.findall(r'/static/contentImg/.+?&#34',content) # 특정 문자열 사이의 단어를 반환
    removeStringPath=[x.replace('/static/contentImg/','') for x in removeStringBetween] # 문자열의 패스제거
    return [x.replace('&#34','') for x in removeStringPath] # 문자열의 불필요한 뒷부분 제거후 최종파일명
    
# 게시글의 타이틀 이미지 추출
def getTitleImage():
    return'defaultImg/titleImage_'+str(random.randrange(1,8))+'.jpg' # 타이틀 이미지 , 없을 경우에 기본 타이틀이미지 1~8중 임의선택 

# 임시이미지 파일을 저장용 폴더에 이동
def moveImageTempToDest(imageFileNames):
    imageForder, fileTempPath, fileDestPath = imageConfig() # 이미지 설정부분
    # 파일 이동 실행 부분
    for imageFile in imageForder:
        if imageFile in imageFileNames:
            shutil.move(fileTempPath + imageFile, fileDestPath + imageFile) # 파일이동

'''
 아래는 보안에 관련된 공통항목이다
 xssFilter
'''
# jinja를 이용한 xss필터함수
def xssFilter(args):
    return str(utils.escape(args))  

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
'''
# 파이어베이스 유저정보 취득
def getUser(uid):
     # 파이어베이스 유저정보
    userInfo={
        'nickname':None,
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