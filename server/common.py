import time
import traceback
import simplejson as json  # dumps(객체) ->json문자열 , loads(json문자열) ->객체
import configparser  # 환경설정파일parser
import base64
from database import Connection

# 메소드데코레이터
def decorate(func):
    print("##### 메소드 시작 => ("+func.__name__+")#####")
    start = time.time()
    end = time.time()
    print("##### 메소드 종료 #####")
    print("소요시간: %5f" % (end-start))

# 이미지파일을 base64형식변환
def imageParser(src):
    with open(src, "rb") as image_file:
        # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
        return "data:image/jpeg;base64, " + \
            base64.b64encode(image_file.read()).decode('utf-8')

# 코드와 맵핑된 에러메세지 반환
def getErrorMessager(errCode, param):
    ERROR_MESSAGE = {
        100: f"{param}を入力してください",
        101: "エラーメッセージてすと",
        200: "エラーメッセージてすと",
    }
    return {
        "errCode": errCode,
        "message": ERROR_MESSAGE[errCode]
    }

# 유저에러_Exception상속
class UserError(Exception):
    # 인스턴스 생성시 리턴되는 인스턴스변수
    def __init__(self, errCode, param):
        self.errorInfo = getErrorMessager(errCode, param)
        
    # 객체가 print함수에 호출될때 표시되는 함수
    def __str__(self):
        return self.errorInfo['message']