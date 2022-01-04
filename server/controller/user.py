from flask import Blueprint, request, jsonify, send_from_directory
from model import userModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
user_controller = Blueprint('user', __name__)


@user_controller.route('/user', methods=['POST', 'DELETE'])
@check_token
@exception_handler
def user():
    '''회원등록'''
    if request.method == 'POST':
        user=request.user #파이어베이스 유저정보 취득

        #기존 등록된 유저여부체크
        isUser=userModel.checkUser(user)
        if not isUser:
            #유저등록
            userModel.insertUser(user)
        else:
            #유저등록에러
            raise UserError(704)

        
        return jsonify(getMessage(601)), 200

    '''회원삭제'''
    if request.method == 'DELETE':
        user=request.user #파이어베이스 유저정보 취득

        #기존 등록된 유저여부체크
        isUser=userModel.checkUser(user)
        if isUser:
            #유저삭제
            userModel.deleteUser(user)
        else:
            #유저삭제에러
            raise UserError(706)
        
        return jsonify(getMessage(601)), 200

@user_controller.route('/userImage', methods=['GET'])
@exception_handler
def userImage():
    '''유저이미지반환'''
    if request.method == 'GET':
        fileName=request.args.get('filename') # 요청URL에서 취득한 파일명
        imageFilePath="static/userImg/"+fileName # 이미지파일 경로
        
        return send_from_directory(imageFilePath) # send_file()은 보안적으로 취약함