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
