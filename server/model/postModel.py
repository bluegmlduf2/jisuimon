from common import *


def getPosts():
    conn = Connection()
    if conn:
        try:
            # 메인화면에 표시할 방정보 8개 가져오기
            sql = '''
            SELECT
                P.post_id,
                P.title,
                P.create_date,
                P.update_date,
                P.title_image,
                P.user_table_user_id,
                U.nickname ,
                U.user_image ,
                PD.content
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.user_table AS U ON
                P.user_table_user_id = U.user_id
            INNER JOIN jisuimon.post_detail_table AS PD ON
                P.post_id = PD.post_table_post_id
            ORDER BY
                P.create_date DESC
            LIMIT 8
            '''

            data = conn.executeAll(sql)
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

def getPostDetail(args):
    conn = Connection()
    if conn:
        try:
            # 게시물의 상세정보
            sql = '''
            SELECT
                P.post_id,
                P.title,
                P.create_date,
                P.update_date,
                P.title_image,
                P.user_table_user_id,
                PD.content
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.post_detail_table AS PD ON
                P.post_id = PD.post_table_post_id
            WHERE
                post_id = "%%{post_id}%%"
            '''.format(post_id=args['post_id'])

            data = conn.executeAll(sql)
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

def getPostIngredient(args):
    conn = Connection()
    if conn:
        try:
            # 게시물의 재료정보
            sql = '''
                SELECT
                    I.ingredient_id ,
                    I.ingredient_name
                FROM
                    jisuimon.post_table AS P
                INNER JOIN jisuimon.ingredient_table AS I ON
                    P.post_id = I.post_table_post_id
                WHERE
                    post_id = "%%{post_id}%%"
                '''.format(
                post_id=args['post_id'])

            data = conn.executeAll(sql)
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

def getPostComment(args):
    conn = Connection()
    if conn:
        try:
            # 게시물의 상세정보
            sql = '''
                SELECT
                    C.comment_content ,
                    C.comment_create_date ,
                    C.comment_id ,
                    C.user_table_user_id ,
                    C.post_table_post_id ,
                    CR.comment_reply_content ,
                    CR.comment_reply_create_date ,
                    CR.commont_reply_id ,
                    CR.user_table_user_id 
                FROM
                    jisuimon.comment_table AS C
                LEFT JOIN jisuimon.commont_reply_table AS CR ON
                    C.comment_id = CR.comment_table_comment_id 
                WHERE
                    C.post_table_post_id = "%%{post_id}%%"   
                '''.format(
                post_id=args['post_id'])

            data = conn.executeAll(sql)
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

def getInputRooms(args):
    conn = Connection()
    if conn:
        try:
            # 방정보가져오기
            sql = '''SELECT
                roomId,
                houseType1,
                houseType2,
                post,
                city1,
                city2,
                city3,
                title,
                content,
                memberId,
                regDate,
                adStatus
            FROM
                house.room
            WHERE
                city1 LIKE "%%{city1}%%"
                OR city2 LIKE "%%{city2}%%"
                OR city3 LIKE "%%{city3}%%"
                OR title LIKE "%%{title}%%"
                OR content LIKE "%%{content}%%"
                AND adStatus=1
            '''.format(
                city1=args['inputValue'], city2=args['inputValue'], city3=args['inputValue'], title=args['inputValue'], content=args['inputValue'])

            data = conn.executeAll(sql)
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
