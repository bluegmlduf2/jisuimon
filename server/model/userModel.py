from common import *

def checkUser(args):
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
