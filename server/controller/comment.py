from flask import Blueprint, request, jsonify
from model import commentModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
comment_controller = Blueprint('comment', __name__)

@comment_controller.route('/comment', methods=['POST'])
@exception_handler
def comment():
    '''댓글 등록'''
    if request.method == 'POST':
        args = request.get_json()

        # xssFilter처리된 값
        filteredArgs={}
        filteredArgs['userId'] = xssFilter(args['userId'])  # 유저아이디
        filteredArgs['commentContent'] = xssFilter(args['commentContent'])  # 댓글내용

        ### 유효성검사 ###
        # 공백 및 비어있는지 체크
        if not filteredArgs['userId']:
            raise UserError(701, 'ユーザーID')
        if not filteredArgs['commentContent']:
            raise UserError(701, 'コメント')

        '''게시물 입력'''
        commentModel.insertComment(filteredArgs)
        
        return jsonify(getMessage(601)), 200
