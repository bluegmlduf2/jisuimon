from model import foodModel
from common import *

# 라우팅 기본경로 table을 가지는 블루프린터 객체를 생성
food_controller = Blueprint('food', __name__)


@food_controller.route('/food', methods=['GET'])
@exception_handler
def food():
    '''음식검색결과'''
    if request.method == 'GET':
        args = request.args
        data = foodModel.getFood(args)  # 음식검색결과정보
        return jsonify(data), 200
