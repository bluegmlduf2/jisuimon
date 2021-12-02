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
        data = postModel.getPosts()

        # 이미지->바이너리(base64)->utf-8문자열
        for i, e in enumerate(data):
            # 타이틀 이미지
            src = current_app.root_path+"/assets/contentImg/"+e['title_image']
            with open(src, "rb") as image_file:
                # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
                data[i]['title_image'] = "data:image/jpeg;base64, " + \
                    base64.b64encode(image_file.read()).decode('utf-8')

            # 유저 이미지
            if not e['user_image']:
                src = current_app.root_path+"/assets/defaultImg/noUser.png"
            else:
                src = current_app.root_path+"/assets/userImg/"+e['user_image']
            with open(src, "rb") as image_file:
                # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
                data[i]['user_image'] = "data:image/jpeg;base64, " + \
                    base64.b64encode(image_file.read()).decode('utf-8')

        return jsonify(data), 200

    '''게시물 등록'''
    if request.method == 'POST':
        args = request.get_json()
        args = request.form

        # 화면에서 받은 값
        title = args['title']  # 제목
        content = args['content']  # 글내용
        ingredient = args['ingredientList']  # 재료정보

        ### 유효성검사 ###
        # 공백 및 비어있는지 체크
        if not title:
            raise UserError(701, 'タイトル')
        if not content:
            raise UserError(701, '作り方')
        if not ingredient:
            raise UserError(701, '材料')

        # #파일존재유무체크
        # for i in range(1,3):
        #     source=current_app.root_path+'/temp/'+args['fileNm'+str(i)]#임시파일저장경로
        #     if os.path.isfile(source) == False:
        #         raise FileNotFoundError

        # '''유저아이디 획득'''
        # args['userId']=sell.getMemberId(args)

        # '''등록한 방의 수 확인 '''
        # if sell.chekRegRoomCnt(args)>0:
        #     raise UserError('一般顧客が登録できる物件は一件のみです。')

        # '''방정보입력'''
        # sell.insertRoom(args)

        # #파일이동
        # for i in range(1,3):
        #     source=current_app.root_path+'/temp/'+args['fileNm'+str(i)]#임시파일저장경로
        #     dest =current_app.root_path+"/saveImage/"+args['fileNm'+str(i)]#최종저장경로
        #     shutil.move(source,dest)# 파일이동
        return jsonify(getMessage(601)), 200


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

        source = current_app.root_path+'/assets/temp/'+resize_image_fileNm  # 임시파일저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        image.convert('RGB').save(source)  # resize사용시 image -> resize_image

        return jsonify(), 200
