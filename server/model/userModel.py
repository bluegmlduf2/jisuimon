from common import *


def checkUser(args):
    '''기존유저존재유무체크'''
    conn = Connection()
    if conn:
        try:
            # 기존 등록된 유저 여부 체크
            sql = '''
            SELECT
                COUNT(*) as isUser
            FROM
                jisuimon.user_table ut
            WHERE
                ut.user_id = %s
            '''

            data = conn.executeOne(sql, args['uid'])['isUser']

        except UserError as e:
            return json.dumps({'status': False, 'message': e.msg}), 200
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            return data
        finally:
            conn.close()


def insertUser(args):
    '''유저추가'''
    conn = Connection()
    if conn:
        try:
            # 유저등록
            sql = '''
            INSERT
                INTO
                jisuimon.user_table (
                user_id)
            VALUES(
                %s);
            '''
            conn.execute(sql, (args['uid']))
        except UserError as e:
            conn.rollback()
            return json.dumps({'status': False, 'message': e.msg}), 200
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def deleteUser(args):
    '''유저삭제'''
    conn = Connection()
    if conn:
        try:
            # 유저삭제
            sql = '''
            DELETE FROM jisuimon.user_table
            WHERE user_id=%s;
            '''
            conn.execute(sql, (args['uid']))

            # 삭제유저의 프로필이미지 삭제
            deleteCurrentUserImage(args)

            # 유저삭제(파이어베이스)
            current_app.auth.delete_user(args['uid'])

        except UserError as e:
            conn.rollback()
            return json.dumps({'status': False, 'message': e.msg}), 200
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def insertUserImage(args):
    '''유저이미지 추가'''
    try:
        # 파일명변경
        resize_image_fileNm = getUUID()+".jpg"  # 파일명변경

        # 리사이즈
        image = Image.open(args['file'])
        resize_image = image.resize((160, 160))  # 160,160 이미지 사이즈변경
        source = current_app.userImgPath+resize_image_fileNm  # 유저이미지저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        resize_image.convert('RGB').save(source)

        # 현재 유저의 지난 프로필이미지 삭제
        deleteCurrentUserImage(args)

        # 파이어베이스에 유저이미지명 등록 (url형식만등록허용함)
        current_app.auth.update_user(
            args['uid'],
            photo_url='http://'+resize_image_fileNm)

    except UserError as e:
        return json.dumps({'status': False, 'message': e.msg}), 200
    except Exception as e:
        traceback.print_exc()
        raise e


def deleteUserImage(args):
    '''유저이미지 삭제'''
    try:
        # 현재 유저의 지난 프로필이미지 삭제
        deleteCurrentUserImage(args)

        # SDK9의 파이선용 삭제 속성
        deleteAttr = current_app.auth.DELETE_ATTRIBUTE

        # 파이어베이스에 유저 이미지 삭제
        current_app.auth.update_user(
            args['uid'],
            photo_url=deleteAttr)

    except UserError as e:
        return json.dumps({'status': False, 'message': e.msg}), 200
    except Exception as e:
        traceback.print_exc()
        raise e


def deleteCurrentUserImage(args):
    '''현재 유저의 프로필이미지 삭제'''
    # 유저 기존 이미지명 취득 (파이어베이스)
    user=getUser(args['uid']) # 유저정보취득 (파이어베이스)
    filePath = current_app.userImgPath+user['user_image']

    # 기존 유저이미지파일 존재시 삭제
    if os.path.exists(filePath) and user['user_image']:
        os.remove(filePath)
