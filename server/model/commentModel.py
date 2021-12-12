from common import *

def insertComment(args):
    conn = Connection()
    if conn:
        try:
            imageFileNames=imageFromContent(args['content']) # 게시글에서 이미지 추출
            # titleImage=getTitleImage(imageFileNames) # 게시글의 타이틀 이미지명 추출

            # 타이틀이미지가 존재할 경우 해당 이미지 사용
            titleImage='' 
            if imageFileNames :
                titleImage=imageFileNames[0]

            # 게시물의 정보
            sql = '''
            INSERT
                INTO
                jisuimon.post_table (
                title,
                create_date,
                update_date,
                title_image,
                user_table_user_id)
            VALUES(
                %s,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                %s,
                1);
            '''

            conn.execute(sql, (args['title'],titleImage))
            insertedPostId = conn.insertLastKey()  # 입력한 부모게시글의 PK

            # 게시물의 상세정보
            sql = '''
            INSERT
                INTO
                jisuimon.post_detail_table (
                post_table_post_id,
                content
                )
            VALUES(
                %s,
                %s
            );
            '''

            conn.execute(sql, (insertedPostId, args['content']))

            # 게시물의 재료정보
            sql = '''
            INSERT
                INTO
                jisuimon.ingredient_table (
                post_table_post_id,
                ingredient_id,
                ingredient_name,
                ingredient_amt,
                ingredient_unit
                )
            VALUES(
                %s,
                %s,
                %s,
                %s,
                %s);
            '''

            # 재료를 한번에 입력하기 (리스트->튜플)
            ingredientList = [(insertedPostId, e['food_id'], e['food_name'],
                               e['food_amt'], e['food_unit']) for e in args['ingredientList']]
            conn.executeMany(sql, ingredientList)
            
            moveImageTempToDest(imageFileNames) # 임시이미지 파일을 저장용 폴더에 이동
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