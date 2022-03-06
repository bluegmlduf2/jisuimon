from numpy import delete
from common import *

def getPosts(args):
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
                U.user_id ,
                PD.content ,
                (
                SELECT
                    COUNT(C.post_table_post_id)
                FROM
                    jisuimon.comment_table AS C
                WHERE
                    C.post_table_post_id = P.post_id) AS comment_cnt ,
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
            LIMIT %s,%s
            '''
            fromPostCnt=int(args['postCnt'])-8
            toPostCnt=8 # 8개씩 가져옴
            data = conn.executeAll(sql, (fromPostCnt,toPostCnt))

            # TODO 유저삭제하면 uid가 없는데 그에대한 대처필요

            removePostCol = ['user_id','user_table_user_id','update_date'] # 불필요한칼럼 (사용자정보)

            # 이미지->바이너리(base64)->utf-8문자열
            for i, e in enumerate(data):
                user=getUser(e['user_id']) # 유저정보취득 (파이어베이스)
                data[i]['nickname']=user['nickname'] # 유저 닉네임
                data[i]['user_image']=user['user_image'] # 유저 프로필이미지
                    
                # 타이틀 이미지
                data[i]['title_image'] = getTitleImage(e)

                # 게시물 내용 변환 escapeHTML->HTML
                data[i]['content'] = htmlUnescape(e['content'])

                # 유저 이미지
                userImagePath = getUserImage(e['user_image'])

                # 섬네일이미지변환Base64
                data[i]['user_image'] = imageParser(userImagePath)

                # 불필요한 게시물의 칼럼제거
                [data[i].pop(colNm) for colNm in removePostCol]


        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            return data
        finally:
            conn.close()


def getPostList(args):
    conn = Connection()
    if conn:
        try:
            # 게시물 리스트 화면에 표시할 게시물 5개 가져오기 (타임존때문에 -9 시간값을 반환)
            sql = '''
            SELECT
                P.post_id,
                P.title,
                CONVERT_TZ(P.create_date, '+00:00', '-09:00') as create_date,
                CONVERT_TZ(P.update_date, '+00:00', '-09:00') as update_date,
                P.user_table_user_id,
                U.user_id ,
                PD.content ,
                (
                SELECT
                    COUNT(C.post_table_post_id)
                FROM
                    jisuimon.comment_table AS C
                WHERE
                    C.post_table_post_id = P.post_id) AS comment_cnt ,
                (
                SELECT
                    COUNT(L.post_table_post_id)
                FROM
                    jisuimon.post_like_table AS L
                WHERE
                    post_table_post_id = P.post_id) AS like_cnt 
                    /*(최초에 8행의 결과가 나온후 각 행마다 위의 서브쿼리를 실행하기때문에 post_table_post_id = P.post_id가 가능하다)*/
            '''

            # 총 게시물의 수 취득용 쿼리
            sqlPostCnt = '''
            SELECT
            COUNT(*) as postCntAll
            '''

            fromPostCnt = int(args['postCnt'])-5
            toPostCnt = 5  # 5개씩 가져옴
            login_user = request.user['uid']  # 파이어베이스 로그인 유저의 uid 취득
            data = None
            postCountData = 0  # 현재 조건의 총 게시물 수

            # 음식명으로 필터 검색시
            if args['ingredientId']:
                # 게시물의 조건
                sqlWhere = '''
                FROM
                    jisuimon.post_table AS P
                INNER JOIN jisuimon.user_table AS U ON
                    P.user_table_user_id = U.user_id
                INNER JOIN jisuimon.post_detail_table AS PD ON
                    P.post_id = PD.post_table_post_id
                LEFT JOIN jisuimon.ingredient_table AS I ON
                    P.post_id = I.post_table_post_id
                WHERE user_id = %s
                AND I.ingredient_id = %s
                ORDER BY
                    P.create_date DESC
                '''

                # 게시물의 취득개수
                sqlLimit = '''
                LIMIT %s,%s
                '''

                # 게시물 가져오기
                sql = sql + sqlWhere + sqlLimit
                data = conn.executeAll(
                    sql, (login_user, args['ingredientId'], fromPostCnt, toPostCnt))

                # 게시물의 총 갯수 가져오기
                sql = sqlPostCnt + sqlWhere
                postCountData = conn.executeOne(
                    sql, (login_user, args['ingredientId']))['postCntAll']
            else:
                # 일반검색시
                # 게시물의 조건
                sqlWhere = '''
                FROM
                    jisuimon.post_table AS P
                INNER JOIN jisuimon.user_table AS U ON
                    P.user_table_user_id = U.user_id
                INNER JOIN jisuimon.post_detail_table AS PD ON
                    P.post_id = PD.post_table_post_id
                WHERE user_id = %s
                ORDER BY
                    P.create_date DESC
                '''

                # 게시물의 취득개수
                sqlLimit = '''
                LIMIT %s,%s
                '''

                # 게시물 가져오기
                sql = sql + sqlWhere + sqlLimit
                data = conn.executeAll(
                    sql, (login_user, fromPostCnt, toPostCnt))

                # 게시물의 총 갯수 가져오기
                sql = sqlPostCnt + sqlWhere
                postCountData = conn.executeOne(
                    sql, (login_user))['postCntAll']

            removePostCol = ['user_id', 'user_table_user_id',
                             'update_date']  # 불필요한칼럼 (사용자정보)

            # 게시물 형식변환과 불필요한 칼럼제거
            for i, e in enumerate(data):
                data[i]['content'] = htmlUnescape(
                    e['content'])  # 게시물 내용 변환 escapeHTML->HTML
                [data[i].pop(colNm)
                 for colNm in removePostCol]  # 불필요한 게시물의 칼럼제거

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            return data, postCountData
        finally:
            conn.close()


def getPostSearch(args):
    conn = Connection()
    if conn:
        try:
            # 게시물 리스트 화면에 표시할 게시물 5개 가져오기 (타임존때문에 -9 시간값을 반환)
            sql = '''
            SELECT
                P.post_id,
                P.title,
                CONVERT_TZ(P.create_date, '+00:00', '-09:00') as create_date,
                CONVERT_TZ(P.update_date, '+00:00', '-09:00') as update_date,
                P.user_table_user_id,
                U.user_id ,
                PD.content ,
                (
                SELECT
                    COUNT(C.post_table_post_id)
                FROM
                    jisuimon.comment_table AS C
                WHERE
                    C.post_table_post_id = P.post_id) AS comment_cnt ,
                (
                SELECT
                    COUNT(L.post_table_post_id)
                FROM
                    jisuimon.post_like_table AS L
                WHERE
                    post_table_post_id = P.post_id) AS like_cnt 
            '''

            # 총 게시물의 수 취득용 쿼리
            sqlPostCnt = '''
                SELECT
                COUNT(*) as postCntAll
            '''

            fromPostCnt = int(args['postCnt'])-5
            toPostCnt = 5  # 5개씩 가져옴
            data = None
            postCountData = 0  # 현재 조건의 총 게시물 수

            # 게시물의 조건
            sqlWhere = '''
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.user_table AS U ON
                P.user_table_user_id = U.user_id
            INNER JOIN jisuimon.post_detail_table AS PD ON
                P.post_id = PD.post_table_post_id
            LEFT JOIN jisuimon.ingredient_table AS I ON
                P.post_id = I.post_table_post_id
            WHERE I.ingredient_id = %s
            ORDER BY
                P.create_date DESC
            '''

            # 게시물의 취득개수
            sqlLimit = '''
            LIMIT %s,%s
            '''

            # 게시물 가져오기
            sql = sql + sqlWhere + sqlLimit
            data = conn.executeAll(
                sql, (args['ingredientId'], fromPostCnt, toPostCnt))

            # 게시물의 총 갯수 가져오기
            sql = sqlPostCnt + sqlWhere
            postCountData = conn.executeOne(
                sql, (args['ingredientId']))['postCntAll']

            removePostCol = ['user_id', 'user_table_user_id',
                             'update_date']  # 불필요한칼럼 (사용자정보)

            # 게시물 형식변환과 불필요한 칼럼제거
            for i, e in enumerate(data):
                data[i]['content'] = htmlUnescape(
                    e['content'])  # 게시물 내용 변환 escapeHTML->HTML
                [data[i].pop(colNm)
                 for colNm in removePostCol]  # 불필요한 게시물의 칼럼제거

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            return data, postCountData
        finally:
            conn.close()


def getPostCount():
    conn = Connection()
    if conn:
        try:
            # 총 게시물 수 구하기
            sql = '''
            SELECT
                COUNT(*) as postCntAll
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.user_table AS U ON
                P.user_table_user_id = U.user_id
            '''

            data = conn.executeOne(sql)

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
            calledMethodName=inspect.stack()[1][3] # 해당 메서드를 호출한 메서드명 (컨트롤러명)
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
                U.user_id 
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

            # 존재하지않는게시물일때 에러반환
            if data is None:
                raise UserError(803)
                
            login_user = None # 로그인 유저 정보

            # 게시물의 수정용 상세정보를 취득
            if calledMethodName == "postDetailUpdate":
                login_user = request.user  # 파이어베이스 유저정보 취득
                # 로그인한 유저와 게시물 작성 유저가 일치하지 않을 경우 예외처리 (부정접근처리)
                if not getUserAuth(login_user,data['user_id']) :
                    raise UserError(802)
            # 일반 게시물 상세정보를 취득
            else:
                login_user = args.user # 파이어베이스 유저정보 취득

            # 게시물 내용 변환 escapeHTML->HTML
            data['content'] = htmlUnescape(data['content'])

            # 파이어베이스 유저정보 취득
            user=getUser(data['user_id']) # 유저정보취득 (파이어베이스)
            data['nickname']=user['nickname'] # 유저 닉네임
            data['user_image']=user['user_image'] # 유저 프로필이미지
            data['post_auth']= getUserAuth(login_user,data['user_id']) # 게시물의 유저권한취득
            
            # 불필요한 게시물의 칼럼제거
            removePostCol = ['user_id','user_table_user_id']
            [data.pop(colNm) for colNm in removePostCol]

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
                    F.food_name as ingredient_name ,
                    I.ingredient_amt ,
                    I.ingredient_unit
                FROM
                    jisuimon.post_table AS P
                INNER JOIN jisuimon.ingredient_table AS I ON
                    P.post_id = I.post_table_post_id
                INNER JOIN jisuimon.food_table AS F ON
                    F.food_id = I.ingredient_id
                WHERE
                    post_id = %s
                '''

            data = conn.executeAll(sql, args['postId'])

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
                    CONVERT_TZ(IFNULL(C.comment_update_date,C.comment_create_date) , 
                    '+00:00', 
                    '-09:00') as comment_create_date,
                    C.comment_id ,
                    C.user_table_user_id ,
                    C.post_table_post_id ,
                    U.user_id ,
                    CR.comment_reply_content ,
                    CONVERT_TZ(IFNULL(CR.comment_reply_update_date,CR.comment_reply_create_date), 
                    '+00:00', 
                    '-09:00') as comment_reply_create_date,
                    CR.comment_reply_id ,
                    CR.comment_table_comment_id,
                    (SELECT user_id FROM user_table AS SU WHERE SU.user_id = CR.user_table_user_id ) AS user_id_CR
                FROM
                    jisuimon.comment_table AS C
                LEFT JOIN jisuimon.comment_reply_table AS CR ON
                    C.comment_id = CR.comment_table_comment_id
                LEFT JOIN jisuimon.user_table AS U ON
                    C.user_table_user_id = U.user_id
                WHERE
                    C.post_table_post_id = %s
                ORDER BY C.comment_create_date , CR.comment_reply_create_date
                '''
            data=conn.executeAll(sql,args['postId'])

            # 유저의 닉네임과 프로필이미지를 파이어베이스로 부터 취득
            for i, e in enumerate(data):
                # 댓글유저정보취득
                user=getUser(e['user_id']) # 댓글유저정보취득 (파이어베이스)
                data[i]['nickname']=user['nickname'] # 유저 닉네임
                data[i]['user_image']=user['user_image'] # 유저 프로필이미지
                # 대댓글유저정보취득
                user_cr=getUser(e['user_id_CR']) # 대댓글유저정보취득 (파이어베이스)
                data[i]['nickname_CR']=user_cr['nickname'] # 유저 닉네임
                data[i]['user_image_CR']=user_cr['user_image'] # 유저 프로필이미지

            # 화면에 반환할 값 commentReturnData
            commentData=list({e['comment_id']:e for e in data}.values()) # 중복 제거한 댓글목록
            commentReturnData=copy.deepcopy(commentData) # ValueError: Circular reference detected 방지..

            # 댓글과 대댓글에서 삭제할 칼럼목록
            removeCommentCol = ['comment_reply_content', 'comment_reply_create_date', 'comment_reply_id',
                                'comment_table_comment_id', 'user_image_CR', 'nickname_CR', 'user_id', 'user_id_CR', 'user_table_user_id','post_table_post_id']
            removeCommentReplyCol = ['comment_content', 'comment_create_date',
                                     'user_table_user_id', 'post_table_post_id', 'user_image', 'nickname', 'user_id', 'user_id_CR']

            # 이미지 경로
            userImgPath=current_app.userImgPath # 유저이미지 경로
            userDefaultImg=current_app.userDefaultImg # 기본 유저이미지 경로            

            # 댓글에 대댓글 추가
            # 댓글 (부모)
            for i,comment in enumerate(commentData):
                commentReturnData[i].setdefault('comment_reply',[])# 대댓글 추가에 필요한 키 추가
                commentReturnData[i].setdefault('showState',False)# 댓글 접고 펼치기에 필요한 키 추가
                commentReturnData[i].setdefault('updateState',False)# 댓글 수정창 토글기능에 필요한 키 추가
                userImage=commentReturnData[i]['user_image'] # 유저 이미지 (댓글유저)
                commentReturnData[i]['user_image']=imageParser(userImgPath+userImage if userImage else userDefaultImg) # 유저 이미지 파싱
                commentReturnData[i]['comment_auth'] = getUserAuth(args.user,commentReturnData[i]['user_id'])# 댓글의 유저권한취득
                [commentReturnData[i].pop(colNm) for colNm in removeCommentCol] # 불필요한 댓글의 칼럼제거
                # 대댓글(자식)
                for commentReply in data:
                    # 댓글과 대댓글이 부모자식관계가 맞을 시 해당 부모 댓글안에 자식 대댓글 딕셔너리를 넣어줌 
                    if comment['comment_id']==commentReply['comment_table_comment_id']:
                        userReplyImage=commentReply['user_image_CR'] # 유저 이미지 (대댓글유저)
                        commentReply['updateState']=False # 대댓글 수정창 토글기능에 필요한 키 추가
                        commentReply['user_image_CR']=imageParser(userImgPath+userReplyImage if userReplyImage else userDefaultImg) # 유저 이미지 (대댓글유저)
                        commentReply['comment_reply_auth'] = getUserAuth(args.user,commentReply['user_id_CR'])# 댓글의 유저권한취득
                        [commentReply.pop(colNmRep) for colNmRep in removeCommentReplyCol] # 불필요한 대댓글의 칼럼제거
                        commentReturnData[i]['comment_reply'].append(commentReply) # 댓글에 해당하는 대댓글 추가

                showReplyState=True if commentReturnData[i]['comment_reply' ] else False # 대댓글이 존재하면 작성창 펼친상태 없으면 닫힌상태
                commentReturnData[i].setdefault('showReplyState',showReplyState)# 대댓글 작성창 접고 펼치기에 필요한 키 추가

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
            imageFileNames=imageFromContent(args['content']) # 게시글에서 이미지 추출

            # 타이틀이미지가 존재할 경우 해당 이미지 사용
            titleImage='' 
            if imageFileNames :
                titleImage=imageFileNames[0]

            # 게시물의 정보
            sql = '''
            INSERT
                INTO
                jisuimon.post_table (
                post_id,
                title,
                create_date,
                update_date,
                title_image,
                user_table_user_id)
            VALUES(
                %s,
                %s,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                %s,
                %s);
            '''
            postId=getUUID() # 게시글 PK
            conn.execute(sql, (postId,args['title'],titleImage,args['userId']))

            # 게시물의 상세정보
            sql = '''
            INSERT
                INTO
                jisuimon.post_detail_table (
                post_detail_id,
                post_table_post_id,
                content
                )
            VALUES(
                %s,
                %s,
                %s
            );
            '''

            postDetailId=getUUID() # 게시글 상세 PK
            conn.execute(sql, (postDetailId, postId, args['content']))

            # 게시물의 재료정보
            sql = '''
            INSERT
                INTO
                jisuimon.ingredient_table (
                post_table_post_id,
                ingredient_id,
                ingredient_amt,
                ingredient_unit
                )
            VALUES(
                %s,
                %s,
                %s,
                %s);
            '''

            # 재료를 한번에 입력하기 (리스트->튜플)
            ingredientList = [(postId, e['food_id'],
                               e['food_amt'], e['food_unit']) for e in args['ingredientList']]
            conn.executeMany(sql, ingredientList)
            
            moveImageTempToDest(imageFileNames) # 임시이미지 파일을 저장용 폴더에 이동
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def updatePost(args):
    conn = Connection()
    if conn:
        try:

            # 수정되기 전 게시물의 이미지 추출용
            sql = '''
                SELECT
                    PD.content 
                FROM
                    jisuimon.post_table AS P
                INNER JOIN jisuimon.post_detail_table AS PD ON
                    P.post_id = PD.post_table_post_id
                WHERE
                    P.post_id = %s
            '''

            data = conn.executeOne(sql, args['postId'])
            imageFileNamesBefore = imageFromContent(data['content']) # 수정되기 전 게시물의 이미지 추출
            imageFileNamesAfter=imageFromContent(args['content']) # 수정된 게시글에서 이미지 추출

            # 수정된 게시글에서 이미지가 존재할 경우 해당 이미지를 타이틀이미지로 사용
            titleImage='' 
            if imageFileNamesAfter :
                titleImage=imageFileNamesAfter[0]

            # 게시물의 수정
            sql = '''
                UPDATE
                    jisuimon.post_table
                SET
                    title = %s,
                    update_date = CURRENT_TIMESTAMP,
                    title_image = %s
                WHERE
                    post_id = %s
                    AND user_table_user_id = %s;
            '''

            conn.execute(sql, (args['title'],titleImage,args['postId'],args['userId']))

            # 게시물의 상세정보 수정
            sql = '''
            UPDATE
                jisuimon.post_detail_table
            SET
                content = %s
            WHERE
                post_table_post_id = %s;
            '''

            conn.execute(sql, (args['content'],args['postId']))

            # 게시물의 재료 삭제
            sql = '''
            DELETE FROM jisuimon.ingredient_table
            WHERE  post_table_post_id=%s;
            '''

            conn.execute(sql, (args['postId']))

            # 게시물의 재료정보
            sql = '''
            INSERT
                INTO
                jisuimon.ingredient_table (
                post_table_post_id,
                ingredient_id,
                ingredient_amt,
                ingredient_unit
                )
            VALUES(
                %s,
                %s,
                %s,
                %s);
            '''

            # 재료를 한번에 입력하기 (리스트->튜플)
            ingredientList = [(args['postId'], e['food_id'],
                               e['food_amt'], e['food_unit']) for e in args['ingredientList']]
            conn.executeMany(sql, ingredientList)
            
            # 삭제된 이미지를 저장된 이미지 파일에서 삭제
            deleteImageFileNames = [image for image in imageFileNamesBefore if image not in imageFileNamesAfter]
            if deleteImageFileNames:
                deleteContentImage(deleteImageFileNames) # 저장용 폴더의 이미지 파일을 삭제

            moveImageTempToDest(imageFileNamesAfter) # 수정한 임시이미지 파일을 저장용 폴더에 이동
        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()


def deletePost(args):
    conn = Connection()
    if conn:
        try:
            # 게시물의 정보
            sql = '''
            SELECT
                P.user_table_user_id as user_id,
                PD.content
            FROM
                jisuimon.post_table AS P
            INNER JOIN jisuimon.post_detail_table AS PD ON
                P.post_id = PD.post_table_post_id
            WHERE
                P.post_id = %s;
            '''

            data = conn.executeOne(sql, args['postId'])
            imageFileNames = imageFromContent(data['content']) # 게시글의 이미지 삭제를 이미지 추출
            login_user = request.user  # 파이어베이스 유저정보 취득

             # 로그인한 유저와 게시물 작성 유저가 일치하지 않을 경우 예외처리 (부정접근처리)
            if not getUserAuth(login_user,data['user_id']) :
                raise UserError(802)
            
            # 게시글의 댓글 정보
            sql = '''
            SELECT
                comment_id
            FROM
                jisuimon.comment_table
            WHERE
                post_table_post_id = %s
            '''
            data = conn.executeOne(sql, args['postId'])

            # 게시물의 댓글이 존재할때 사용
            if data is not None:
                # 게시글의 대댓글 삭제
                sql = '''
                DELETE
                FROM
                    jisuimon.comment_reply_table
                WHERE
                    comment_table_comment_id = %s;
                '''
                conn.execute(sql, (data['comment_id']))

                # 게시글의 댓글 삭제
                sql = '''
                DELETE
                FROM
                    jisuimon.comment_table
                WHERE
                    post_table_post_id = %s;
                '''
                conn.execute(sql, (args['postId']))

            # 게시글의 재료 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.ingredient_table
            WHERE
                post_table_post_id = %s;
            '''
            conn.execute(sql, (args['postId']))

            # 게시글의 좋아요 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.post_like_table
            WHERE
                post_table_post_id = %s;
            '''
            conn.execute(sql, (args['postId']))

            # 게시글의 상세정보 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.post_detail_table
            WHERE
                post_table_post_id = %s;
            '''
            conn.execute(sql, (args['postId']))

            # 게시글 삭제
            sql = '''
            DELETE
            FROM
                jisuimon.post_table
            WHERE
                post_id = %s;
            '''
            conn.execute(sql, (args['postId']))

            # 게시글에 이미지가 존재할시 이미지 삭제
            if imageFileNames:
                deleteContentImage(imageFileNames) # 저장용 폴더의 이미지 파일을 삭제

        except Exception as e:
            traceback.print_exc()
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()

def insertPostTempImage(args):
    '''유저이미지 추가'''
    try:
        # 파일명변경
        now = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=9)))  # 일본시간
        time = now.strftime('%Y%m%d%H%M%S')  # YYYYmmddHHMMSS 형태의 시간 출력
        ranNum = str(random.randint(1, 999999)).rjust(4, "0")  # 난수4자리,공백은0으로채움
        resize_image_fileNm = time+ranNum+".jpg"  # 파일명변경

        # 이미지 저장
        image = Image.open(args['file'])
        source = current_app.fileTempPath+resize_image_fileNm  # 임시파일저장경로

        # RGB형식으로 변경후 , 이미지 파일 저장
        image.convert('RGB').save(source)  # resize사용시 image -> resize_image

    except Exception as e:
        traceback.print_exc()
        raise e
    else:
        return resize_image_fileNm