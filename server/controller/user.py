from model import userModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
user_controller = Blueprint('user', __name__)


@user_controller.route('/user', methods=['POST'])
@exception_handler
def getUser():
    '''회원등록'''
    if request.method == 'POST':
        args = request.get_json()
        
        # 유효성 공백체크
        if not args['email']:
            raise UserError(701, 'Email')

        # 파이어베이스에서 이메일로 유저검색 후 uid 초기화
        user=current_app.auth.get_user_by_email(args['email'])
        args['uid']= user.uid

        # 기존 등록된 유저여부체크
        isUser = userModel.checkUser(args)
        if not isUser:
            # 유저등록
            userModel.insertUser(args)
        else:
            # 유저등록에러
            raise UserError(704)

        return jsonify(getMessage(601)), 200


@user_controller.route('/user', methods=['DELETE'])
@check_token
@exception_handler
def user():
    '''회원삭제'''
    if request.method == 'DELETE':
        user = request.user  # 파이어베이스 유저정보 취득

        # 기존 등록된 유저여부체크
        isUser = userModel.checkUser(user)
        if isUser:
            # 유저삭제
            userModel.deleteUser(user)
        else:
            # 유저삭제에러
            raise UserError(706)

        return jsonify(getMessage(601)), 200


@user_controller.route('/userImage', methods=['GET'])
@exception_handler
def getUserImage():
    '''유저이미지반환'''
    # 토큰사용때문에 userImage메서드와 분리
    if request.method == 'GET':
        fileName = request.args.get('filename')  # 요청URL에서 취득한 파일명
        imageFilePath = "static/userImg/"  # 이미지파일 경로

        # send_file()은 보안적으로 취약함
        return send_from_directory(imageFilePath, fileName)


@user_controller.route('/userImage', methods=['POST', 'DELETE'])
@check_token
@exception_handler
def userImage():
    '''유저이미지입력'''
    if request.method == 'POST':
        # 파일이름 존재체크
        f = request.files['userImage']  # 유저이미지

        if f.filename == '':
            raise UserError(702)

        # 파일 사이즈 체크
        size = len(f.read())

        # 빈파일체크
        if size == 0:
            raise UserError(703)
        
        # 5MB 이상 업로드 방지
        if size > 5242880:
            raise UserError(708)

        args = request.user  # 파이어베이스 유저정보 취득
        args['file'] = f  # 유저 프로필 이미지

        userModel.insertUserImage(args)

        return jsonify(getMessage(601)), 200

    '''유저이미지삭제'''
    if request.method == 'DELETE':
        # 파일이미지명을 파이어베이스와 서버DB에 등록
        args = request.user  # 파이어베이스 유저정보 취득
        userModel.deleteUserImage(args)

        return jsonify(getMessage(601)), 200
