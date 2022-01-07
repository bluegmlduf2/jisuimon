from flask import Blueprint, request, jsonify, send_from_directory
from model import userModel
from PIL import Image  # 이미지 사이즈 변경
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
def getUserImage():
    '''유저이미지반환'''
    # 토큰사용때문에 userImage메서드와 분리
    if request.method == 'GET':
        fileName=request.args.get('filename') # 요청URL에서 취득한 파일명
        imageFilePath="static/userImg/" # 이미지파일 경로
        
        return send_from_directory(imageFilePath,fileName) # send_file()은 보안적으로 취약함
    

@user_controller.route('/userImage', methods=['POST','DELETE'])
@check_token
@exception_handler
def userImage():
    '''유저이미지입력'''
    if request.method == 'POST':
        # 파일이름 존재체크
        f = request.files['userImage'] #유저이미지
        
        if f.filename == '':
            raise UserError(702)

        # 파일 사이즈 체크
        size = len(f.read())

        # 빈파일체크
        if size == 0:
            raise UserError(703)

        # 파일명변경
        resize_image_fileNm = getUUID()+".jpg"  # 파일명변경

        # 리사이즈
        image = Image.open(f)
        resize_image = image.resize((286,180)) # 286,180 이미지 사이즈변경

        source = current_app.userImgPath+resize_image_fileNm  # 유저이미지저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        resize_image.convert('RGB').save(source)
        
        # 파일이미지명을 파이어베이스와 서버DB에 등록
        args=request.user #파이어베이스 유저정보 취득
        args['filename']=resize_image_fileNm # 파일명
        userModel.insertUserImage(args)
        
        # 파일명을 반환
        return jsonify({"url":resize_image_fileNm}), 200