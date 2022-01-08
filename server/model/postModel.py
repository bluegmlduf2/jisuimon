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
 
            # 이미지->바이너리(base64)->utf-8문자열
            for i, e in enumerate(data):
                user = current_app.auth.get_user(e['user_id']) # 유저정보취득 (파이어베이스)
                data[i]['nickname']=user.display_name # 유저 닉네임
                data[i]['user_image']=str(user.photo_url or '').replace(
                    'http://', '') # 유저 프로필이미지
                    
                # 타이틀 이미지
                if not e['title_image']:
                    #　타이틀의 이미지가 없을 경우 기본 이미지를 출력
                    e['title_image']=getTitleImage()
                src = current_app.fileDestPath+e['title_image']
                with open(src, "rb") as image_file:
                    # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
                    data[i]['title_image'] = "data:image/jpeg;base64, " + \
                        base64.b64encode(image_file.read()).decode('utf-8')

                # 유저 이미지
                if not e['user_image']:
                    src = current_app.userDefaultImg
                else:
                    src = current_app.userImgPath+e['user_image']
                with open(src, "rb") as image_file:
                    # b64encode함수는 바이트코드를만든다. decode는 문자열을 만든다.
                    data[i]['user_image'] = "data:image/jpeg;base64, " + \
                        base64.b64encode(image_file.read()).decode('utf-8')

                # 유저 닉네임
                if not e['nickname']:
                    # 유저네임이 존재하지 않는 경우 유저명임의생성 (타임스탬프이용)
                    data[i]['nickname'] = "USER" + str(user.user_metadata.creation_timestamp)
                    
                
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
            '''

            data = conn.executeOne(sql)

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
                    I.ingredient_name ,
                    I.ingredient_amt ,
                    I.ingredient_unit
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
                    CONVERT_TZ(C.comment_create_date, '+00:00', '-09:00') as comment_create_date,
                    C.comment_id ,
                    C.user_table_user_id ,
                    C.post_table_post_id ,
                    U.user_image,
                    U.nickname,
                    CR.comment_reply_content ,
                    CONVERT_TZ(CR.comment_reply_create_date, '+00:00', '-09:00') as comment_reply_create_date,
                    CR.comment_reply_id ,
                    CR.comment_table_comment_id,
                    (SELECT user_image FROM user_table AS SU WHERE SU.user_id = CR.user_table_user_id ) AS user_image_CR,
                    (SELECT nickname FROM user_table AS SU WHERE SU.user_id = CR.user_table_user_id ) AS nickname_CR
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

            # 화면에 반환할 값 commentReturnData
            commentData=list({e['comment_id']:e for e in data}.values()) # 중복 제거한 댓글목록
            commentReturnData=copy.deepcopy(commentData) # ValueError: Circular reference detected 방지..

            # 댓글과 대댓글에서 삭제할 칼럼목록
            removeCommentCol=['comment_reply_content','comment_reply_create_date','comment_reply_id','comment_table_comment_id','user_image_CR','nickname_CR']
            removeCommentReplyCol=['comment_content','comment_create_date','user_table_user_id','post_table_post_id','user_image','nickname']

            # 이미지 경로
            userImgPath=current_app.userImgPath # 유저이미지 경로
            userDefaultImg=current_app.userDefaultImg # 기본 유저이미지 경로            

            # 댓글에 대댓글 추가
            # 댓글 (부모)
            for i,comment in enumerate(commentData):
                commentReturnData[i].setdefault('comment_reply',[])# 대댓글 추가에 필요한 키 추가
                commentReturnData[i].setdefault('showState',False)# 댓글 접고 펼치기에 필요한 키 추가
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
                
                showReplyState=True if commentReturnData[i]['comment_reply'] else False # 대댓글이 존재하면 작성창 펼친상태 없으면 닫힌상태
                commentReturnData[i].setdefault('showReplyState',showReplyState)# 대댓글 작성창 접고 펼치기에 필요한 키 추가

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
                UCvstCIzmxYDWOh9ujTtAYlHsxE3);
            '''
            postId=getUUID() # 게시글 PK
            conn.execute(sql, (postId,args['title'],titleImage))

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
            ingredientList = [(postId, e['food_id'], e['food_name'],
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

    except UserError as e:
        return json.dumps({'status': False, 'message': e.msg}), 200
    except Exception as e:
        traceback.print_exc()
        raise e
    else:
        return resize_image_fileNm