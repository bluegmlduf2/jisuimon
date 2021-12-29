from flask import Blueprint, request, jsonify
from model import userModel
from common import *
import bcrypt  # 암호화
import base64

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
user_controller = Blueprint('user', __name__)


@user_controller.route('/signUp', methods=['POST'])
@exception_handler
def signUp():
    '''회원등록'''
    if request.method == 'POST':
        f = request.files['imageFile']
        # 파일이름 존재체크
        if f.filename == '':
            raise UserError(702)

        # 파일 사이즈 체크
        size = len(f.read())

        # 빈파일체크
        if size == 0:
            raise UserError(703)

        
        return jsonify({"url":dest}), 200