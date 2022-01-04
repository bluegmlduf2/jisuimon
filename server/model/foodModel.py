from common import *


def getFood(args):
    conn = Connection()
    if conn:
        try:
            # 음식검색리스트
            sql = '''
                SELECT
                    FT.food_id ,
                    FT.food_name 
                FROM
                    jisuimon.food_table AS FT
                WHERE
                    MATCH(FT.food_name) AGAINST("%s*" IN BOOLEAN MODE)
                LIMIT 50
                -- 검색어 4글자에서 2글자로
                -- mysql --help | grep my.cnf 에서 ft_min_word_len=2추가
                -- 공백구분가능한 fulltext인덱스 
                -- ALTER TABLE jisuimon.food_table ADD FULLTEXT INDEX idx_foodName_full_text(food_name) WITH PARSER NGRAM
            '''

            data = conn.executeAll(sql, args['food_name'])
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
