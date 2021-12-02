from flask import jsonify
import time
import traceback
import simplejson as json  # dumps(객체) ->json문자열 , loads(json문자열) ->객체
import configparser  # 환경설정파일parser
import base64
from database import Connection
from functools import wraps
from jinja2 import utils # xssFilter

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

# 코드와 맵핑된 메세지 반환
def getMessage(code, param=None):
    MESSAGE = {
        # 성공
        601: "成功しました",
        # 실패 (사용자)
        701: f"{param}を入力してください",
        702: "ファイル名が存在しません。\nファイルアップロード失敗しました",
        703: "空きファイルです。\nファイルアップロード失敗しました",
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
    def __init__(self, errCode, param):
        self.errorInfo = getMessage(errCode, param)

    # 객체가 print함수에 호출될때 표시되는 함수
    def __str__(self):
        return self.errorInfo['message']

'''
 아래는 이미지 파싱에 관련된 공통항목이다
 imageParser
'''
# 이미지파일을 base64형식변환
def imageParser(src):
    with open(src, "rb") as image_file:
        # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
        return "data:image/jpeg;base64, " + \
            base64.b64encode(image_file.read()).decode('utf-8')

'''
 아래는 보안에 관련된 공통항목이다
 imageParser
'''
# jinja를 이용한 xss필터함수
def xssFilter(args):
    return str(utils.escape(args))  