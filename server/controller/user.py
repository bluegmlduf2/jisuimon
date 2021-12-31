from flask import Blueprint, request, jsonify
from model import userModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
user_controller = Blueprint('user', __name__)


@user_controller.route('/signUp', methods=['POST'])
@exception_handler
def signUp():
    '''회원등록'''
    if request.method == 'POST':
        args = request.get_json()
        #기존 등록된 유저여부체크
        isUser=userModel.checkUser(args)
        if not isUser:
            #유저등록
            userModel.insertUser(args)
        else:
            #유저등록에러
            raise UserError(704)

        
        return jsonify(getMessage(601)), 200