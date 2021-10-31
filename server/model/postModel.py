from common import *

def getPosts():
    conn = Connection()
    if conn:
        try:
            #방정보가져오기
            sql = '''SELECT post_id
            , title
            , create_date
            , update_date
            , title_image
            , user_table_user_id
            FROM jisuimon.post_table;
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

def getInputRooms(args):
    conn = Connection()
    if conn:
        try:
            #방정보가져오기
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
                city1=args['inputValue']
                ,city2=args['inputValue']
                ,city3=args['inputValue']
                ,title=args['inputValue']
                ,content=args['inputValue'])

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
