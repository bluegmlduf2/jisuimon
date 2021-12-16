from flask import Blueprint, request, session, current_app, jsonify
from model import postModel
from common import *
import datetime  # 이미지 업로드에서 사용할 시간모듈
from PIL import Image  # 이미지 사이즈 변경
import bcrypt  # 암호화
import base64
import random

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
post_controller = Blueprint('post', __name__)


@post_controller.route('/post', methods=['GET', 'POST'])
@exception_handler
def post():
    '''메인화면의 게시물 8개 가져오기'''
    if request.method == 'GET':
        args = request.args
        data = postModel.getPosts(args)

        return jsonify(data), 200

    '''게시물 등록'''
    if request.method == 'POST':
        args = request.get_json()
        ################
        # args = request.form
        ################

        # 글내용의 이미지 url변경
        filteredContent = args['content'].replace('/static/temp/','/static/contentImg/')
        args['content'] = filteredContent

        # xssFilter처리된 값
        filteredArgs={}
        filteredArgs['title'] = xssFilter(args['title'])  # 제목
        filteredArgs['content'] = xssFilter(args['content'])  # 글내용
        filteredArgs['ingredientList'] = args['ingredientList']  # 재료정보

        ### 유효성검사 ###
        # 공백 및 비어있는지 체크
        if not filteredArgs['title']:
            raise UserError(701, 'タイトル')
        if not filteredArgs['content']:
            raise UserError(701, '作り方')
        if not filteredArgs['ingredientList']:
            raise UserError(701, '材料')

        '''게시물 입력'''
        postModel.insertPost(filteredArgs)
        
        return jsonify(getMessage(601)), 200

@post_controller.route('/postcount', methods=['GET'])
@exception_handler
def postCount():
    '''총 게시물 수 가져오기'''
    if request.method == 'GET':
        data = postModel.getPostCount()
        return jsonify(data), 200


@post_controller.route('/postDetail', methods=['GET'])
@exception_handler
def postDetail():
    '''게시물의 상세정보'''
    if request.method == 'GET':
        args = request.args
        detailData = postModel.getPostDetail(args)  # 게시물 상세정보
        commentData = postModel.getPostComment(args)  # 게시물 댓글정보
        ingredientData = postModel.getPostIngredient(args)  # 게시물 재료정보
        return jsonify(detailData, commentData, ingredientData), 200


@post_controller.route('/imageUploadTemp', methods=['POST'])
@exception_handler
def imageUploadTemp():
    '''게시물 임시이미지 업로드'''
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

        # 파일명변경
        now = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=9)))  # 일본시간
        time = now.strftime('%Y%m%d%H%M%S')  # YYYYmmddHHMMSS 형태의 시간 출력
        ranNum = str(random.randint(1, 999999)).rjust(4, "0")  # 난수4자리,공백은0으로채움
        resize_image_fileNm = time+ranNum+".jpg"  # 파일명변경

        # 리사이즈
        image = Image.open(f)
        # resize_image = image.resize((286,180)) # 286,180 이미지 사이즈변경

        source = current_app.root_path+'/static/temp/'+resize_image_fileNm  # 임시파일저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        image.convert('RGB').save(source)  # resize사용시 image -> resize_image
        
        url=request.host_url # 홈 URL
        # 개발환경용 url 설정
        if current_app.env == 'development':
            url="http://localhost:5000"
        
        # 나중에 같은 서버 사용하면 변경해야함
        dest=url+'/static/temp/'+resize_image_fileNm # 임시 저장 경로
        
        return jsonify({"url":dest}), 200
