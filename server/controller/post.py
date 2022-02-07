from model import postModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
post_controller = Blueprint('post', __name__)


@post_controller.route('/post', methods=['GET'])
@exception_handler
def getPost():
    '''메인화면의 게시물 8개 가져오기'''
    if request.method == 'GET':
        args = request.args
        data = postModel.getPosts(args)

        return jsonify(data), 200


@post_controller.route('/postList', methods=['GET'])
@check_token
@exception_handler
def getPostList():
    '''게시물 리스트 화면의 게시물 5개 가져오기'''
    if request.method == 'GET':
        args = request.args
        postListData = postModel.getPostList(args)

        # 0:게시물정보 , 1:게시물의 수
        return jsonify(postListData[0],postListData[1]), 200


@post_controller.route('/postSearch', methods=['GET'])
@exception_handler
def getPostSearch():
    '''게시물 리스트 화면의 게시물 5개 가져오기'''
    if request.method == 'GET':
        args = request.args
        postSearchData = postModel.getPostSearch(args)

        # 0:게시물정보 , 1:게시물의 수
        return jsonify(postSearchData[0],postSearchData[1]), 200


@post_controller.route('/post', methods=['POST','DELETE'])
@check_token
@exception_handler
def post():
    '''게시물 등록'''
    if request.method == 'POST':
        args = request.get_json()

        # 글내용의 이미지 url변경
        filteredContent = args['content'].replace(
            '/static/temp/', '/static/contentImg/')
        args['content'] = filteredContent

        # xssFilter처리된 값 
        # 프론트의 ckEditor에 의해 특정 html태그(script등..)가 escape되지만 보안을 위해 서버에서 한번 더 처리해줘야한다 
        filteredArgs = {}
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

        filteredArgs['userId'] = request.user['uid']  # 파이어베이스 유저정보 취득

        '''게시물 입력'''
        postModel.insertPost(filteredArgs)

        return jsonify(getMessage(601)), 200
    
    '''게시물 삭제'''
    if request.method == 'DELETE':
        args = request.get_json()
        
        '''게시물 삭제'''
        postModel.deletePost(args)

        return jsonify(getMessage(601)), 200


@post_controller.route('/postcount', methods=['GET'])
@exception_handler
def postCount():
    '''총 게시물 수 가져오기'''
    if request.method == 'GET':
        data = postModel.getPostCount()
        return jsonify(data), 200


@post_controller.route('/postDetail', methods=['GET'])
@get_token
@exception_handler
def postDetail():
    '''게시물의 상세정보'''
    if request.method == 'GET':
        args = request.args
        detailData = postModel.getPostDetail(args)  # 게시물 상세정보
        commentData = postModel.getPostComment(args)  # 게시물 댓글정보
        ingredientData = postModel.getPostIngredient(args)  # 게시물 재료정보
        return jsonify(detailData, commentData, ingredientData), 200


@post_controller.route('/postDetailUpdate', methods=['GET'])
@check_token
@exception_handler
def postDetailUpdate():
    '''게시물의 수정용 상세정보'''
    if request.method == 'GET':
        args = request.args
        detailData = postModel.getPostDetail(args) # 게시물 상세정보
        ingredientData = postModel.getPostIngredient(args) # 게시물 재료정보
        return jsonify(detailData, ingredientData), 200


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

        # 임시파일이미지
        args = {
            'file': f
        }

        # 임시이미지 등록
        resize_image_fileNm = postModel.insertPostTempImage(args)  

        # 임시등록한 이미지의 url+파일명반환
        dest = getUrlPath()+current_app.urlTempPath+resize_image_fileNm  # 임시 저장 경로

        return jsonify({"url": dest}), 200
