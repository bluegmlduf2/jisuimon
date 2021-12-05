from common import *
from flask import current_app
import copy


def getPosts():
    conn = Connection()
    if conn:
        try:
            # 메인화면에 표시할 게시물 8개 가져오기 (타임존때문에 -9 시간값을 반환)
            sql = '''
            SELECT
                P.post_id,
                P.title,
                CONVERT_TZ(P.create_date, '+00:00', '-09:00') as create_date,
                CONVERT_TZ(P.update_date, '+00:00', '-09:00') as update_date,
                P.title_image,
                P.user_table_user_id,
                U.nickname ,
                U.user_image ,
                PD.content ,
                (
                SELECT
                    COUNT(L.post_table_post_id)
                FROM
                    jisuimon.post_like_table AS L
                WHERE
                    post_table_post_id = P.post_id) AS like_cnt 
                    /*(최초에 8행의 결과가 나온후 각 행마다 위의 서브쿼리를 실행하기때문에 post_table_post_id = P.post_id가 가능하다)*/
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
                CONVERT_TZ(P.create_date, '+00:00', '-09:00') as create_date,
                CONVERT_TZ(P.update_date, '+00:00', '-09:00') as update_date,
                P.title_image,
                P.user_table_user_id,
                PD.content,
                U.nickname,
                U.user_image 
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.post_detail_table AS PD ON
                P.post_id = PD.post_table_post_id
            INNER JOIN jisuimon.user_table AS U ON
                P.user_table_user_id = U.user_id 
            WHERE
                post_id = %s
            '''

            data = conn.executeOne(sql, args['postId'])

        except UserError as e:
            conn.rollback()
            raise e
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
                    post_id = %s
                '''

            data = conn.executeAll(sql, args['postId'])

        except UserError as e:
            conn.rollback()
            raise e
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
            # 게시물의 댓글정보
            sql = '''
                 SELECT
                    C.comment_content ,
                    C.comment_create_date ,
                    CONVERT_TZ(C.comment_create_date, '+00:00', '-09:00') as comment_create_date,
                    C.comment_id ,
                    C.user_table_user_id ,
                    C.post_table_post_id ,
                    U.user_image,
                    U.nickname,
                    CR.comment_reply_content ,
                    CONVERT_TZ(CR.comment_reply_create_date, '+00:00', '-09:00') as comment_reply_create_date,
                    CR.commont_reply_id ,
                    CR.comment_table_comment_id,
                    (SELECT user_image FROM user_table AS SU WHERE SU.user_id = CR.user_table_user_id ) AS user_image_CR,
                    (SELECT nickname FROM user_table AS SU WHERE SU.user_id = CR.user_table_user_id ) AS nickname_CR
                FROM
                    jisuimon.comment_table AS C
                LEFT JOIN jisuimon.commont_reply_table AS CR ON
                    C.comment_id = CR.comment_table_comment_id
                LEFT JOIN jisuimon.user_table AS U ON
                    C.user_table_user_id = U.user_id
                WHERE
                    C.post_table_post_id = %s
                ORDER BY C.comment_create_date , CR.comment_reply_create_date
                '''
            data=conn.executeAll(sql,args['postId'])

            # 화면에 반환할 값 commentReturnData
            commentData=list({e['comment_id']:e for e in data}.values()) # 중복 제거한 댓글목록
            commentReturnData=copy.deepcopy(commentData) # ValueError: Circular reference detected 방지..

            # 댓글과 대댓글에서 삭제할 칼럼목록
            removeCommentCol=['comment_reply_content','comment_reply_create_date','commont_reply_id','comment_table_comment_id','user_image_CR','nickname_CR']
            removeCommentReplyCol=['comment_content','comment_create_date','user_table_user_id','post_table_post_id','user_image','nickname']

            # 이미지 경로
            userImgPath=current_app.root_path + "/static/userImg/" # 유저이미지 경로
            userDefaultImg=current_app.root_path+"/static/defaultImg/noUser.png" # 기본 유저이미지 경로            

            # 댓글에 대댓글 추가
            # 댓글 (부모)
            for i,comment in enumerate(commentData):
                commentReturnData[i].setdefault('comment_reply',[])# 대댓글 추가에 필요한 키 추가
                commentReturnData[i].setdefault('showState',False)# 댓글 접고 펼치기에 필요한 키 추가
                commentReturnData[i].setdefault('showReplyState',False)# 대댓글 작성창 접고 펼치기에 필요한 키 추가
                [commentReturnData[i].pop(colNm) for colNm in removeCommentCol] # 불필요한 댓글의 칼럼제거
                userImage=commentReturnData[i]['user_image'] # 유저 이미지 (댓글유저)
                commentReturnData[i]['user_image']=imageParser(userImgPath+userImage if userImage else userDefaultImg)
                # 대댓글(자식)
                for commentReply in data:
                    # 댓글과 대댓글이 부모자식관계가 맞을 시 해당 부모 댓글안에 자식 대댓글 딕셔너리를 넣어줌 
                    if comment['comment_id']==commentReply['comment_table_comment_id']:
                        userReplyImage=commentReply['user_image_CR'] # 유저 이미지 (대댓글유저)
                        commentReply['user_image_CR']=imageParser(userImgPath+userReplyImage if userReplyImage else userDefaultImg) # 유저 이미지 (대댓글유저)
                        [commentReply.pop(colNmRep) for colNmRep in removeCommentReplyCol] # 불필요한 대댓글의 칼럼제거
                        commentReturnData[i]['comment_reply'].append(commentReply) # 댓글에 해당하는 대댓글 추가

        except UserError as e:
            conn.rollback()
            raise e
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            return commentReturnData
        finally:
            conn.close()


def insertPost(args):
    conn = Connection()
    if conn:
        try:
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
                'defaultImage..',
                1);
            '''

            conn.execute(sql, (args['title']))
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
            conn.executeMany(
                sql, ingredientList)
        except UserError as e:
            return json.dumps({'status': False, 'message': e.msg}), 200
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()
