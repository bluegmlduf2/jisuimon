from common import *


def insertComment(args):
    conn = Connection()
    if conn:
        try:

            # 댓글등록
            sql = '''
            INSERT
                INTO
                jisuimon.comment_table (
                comment_id,
                comment_content,
                comment_create_date,
                user_table_user_id,
                post_table_post_id)
            VALUES(
                %s,
                %s,
                CURRENT_TIMESTAMP,
                %s,
                %s
            );
            '''

            commentId = getUUID()  # 댓글의 PK
            conn.execute(
                sql, (commentId, args['commentContent'], args['userId'], args['postId']))
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def updateComment(args):
    conn = Connection()
    if conn:
        try:
            # 댓글수정
            sql = '''
            UPDATE
                jisuimon.comment_table
            SET
                comment_content = %s,
                comment_update_date = CURRENT_TIMESTAMP
            WHERE
                comment_id = %s;
            '''

            conn.execute(
                sql, (args['commentContent'], args['commentId']))
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def deleteComment(args):
    conn = Connection()
    if conn:
        try:
            # 댓글의 정보
            sql = '''
            SELECT
                user_table_user_id as user_id
            FROM
                jisuimon.comment_table as C
            WHERE 
                C.comment_id = %s;
            '''

            data = conn.executeOne(sql, args['commentId'])
            login_user = request.user  # 파이어베이스 유저정보 취득

            # 로그인한 유저와 댓글 작성 유저가 일치하지 않을 경우 예외처리 (부정접근처리)
            if not getUserAuth(login_user, data['user_id']):
                raise UserError(705)

            # 대댓글에 작성자 이외의 댓글이 존재하는지 체크
            sql = '''
                SELECT
                    COUNT(*) as cnt 
                FROM
                    jisuimon.comment_reply_table as CR
                WHERE 
                    CR.comment_table_comment_id = %s
                    AND CR.user_table_user_id != %s;
            '''
            data = conn.executeOne(sql, (args['commentId'], data['user_id']))

            # 대댓글에 작성자 이외의 사람이 대댓글을 남겼을경우 삭제불가
            if data['cnt'] > 0:
                raise UserError(707, 'コメント')

            # 게시글의 대댓글 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.comment_reply_table
            WHERE
                comment_table_comment_id = %s;
            '''
            conn.execute(sql, (args['commentId']))

            # 게시글의 댓글 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.comment_table
            WHERE
                comment_id = %s;
            '''
            conn.execute(sql, (args['commentId']))

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def insertCommentReply(args):
    conn = Connection()
    if conn:
        try:

            # 대댓글등록
            sql = '''
            INSERT
                INTO
                jisuimon.comment_reply_table (
                comment_reply_id,
                comment_reply_content,
                comment_reply_create_date,
                user_table_user_id,
                comment_table_comment_id)
            VALUES(%s,
                %s,
                CURRENT_TIMESTAMP,
                %s,
                %s
            );
            '''

            commentReplyId = getUUID()  # 대댓글의 PK
            conn.execute(
                sql, (commentReplyId, args['commentReplyContent'], args['commentUserId'], args['commentId']))

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def updateCommentReply(args):
    conn = Connection()
    if conn:
        try:
            # 대댓글수정
            sql = '''
            UPDATE
                jisuimon.comment_reply_table
            SET
                comment_reply_content = %s,
                comment_reply_update_date = CURRENT_TIMESTAMP
            WHERE
                comment_reply_id = %s;
            '''

            conn.execute(
                sql, (args['commentReplyContent'], args['commentReplyId']))
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def deleteCommentReply(args):
    conn = Connection()
    if conn:
        try:
            # 대댓글의 정보
            sql = '''
            SELECT
                CR.user_table_user_id as user_id
            FROM
                jisuimon.comment_reply_table as CR
            WHERE
                CR.comment_reply_id = %s;
            '''

            data = conn.executeOne(sql, args['commentReplyId'])
            login_user = request.user  # 파이어베이스 유저정보 취득

            # 로그인한 유저와 대댓글 작성 유저가 일치하지 않을 경우 예외처리 (부정접근처리)
            if not getUserAuth(login_user, data['user_id']):
                raise UserError(705)

            # 게시글의 대댓글 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.comment_reply_table
            WHERE
                comment_reply_id = %s;
            '''
            conn.execute(sql, (args['commentReplyId']))

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()
