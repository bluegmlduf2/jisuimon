from flask import Blueprint, request, session, current_app, jsonify
from model import foodModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
food_controller = Blueprint('food', __name__)

@food_controller.route('/food', methods=['GET'])
def food():
    '''음식검색결과'''
    try:
        if request.method == 'GET':
            args = request.args
            data = foodModel.getFood(args)  # 음식검색결과정보             
    except UserError as e:
        return jsonify(e.errorInfo), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"errCode": 501,"message":"システムエラー"}), 500
    else:
        return jsonify(data), 200
