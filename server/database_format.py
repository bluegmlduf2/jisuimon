import pymysql

class Connection:
    def __init__(self):
        # (인스턴스)멤버변수등록
        self.db = pymysql.connect(host='localhost',
                                  user='',
                                  password='',
                                  db='',
                                  charset='utf8mb4')
        #DB의 커서 선언
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args=()):
        '''execute는 쿼리 실행까지만,값을 가져올때는 fetch를 사용'''
        # execute의 args의 매개변수는 튜플이 들어가야함
        result=self.cursor.execute(query, args) # args를 매개변수로 사용하며 SqlInjection방지
        print(self.cursor._last_executed)
        return result

    def executeMany(self, query, args=()):
        '''executeMany는 다량의 데이터를 한번에 입력'''
        # args의 매개변수는 리스트의 튜플이 들어가야함
        result=self.cursor.executemany(query, args)
        print(self.cursor._last_executed)
        return result

    def executeOne(self, query, args=()):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        print(self.cursor._last_executed)
        return row

    def executeAll(self, query, args=()):
        '''쿼리를 실행한뒤(execute) 모든 값을 받아옴(fetchAll)'''
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        print(self.cursor._last_executed)
        return row

    def insertLastKey(self):
        return self.db.insert_id()

    # 정적메서드_인스턴스화 하지않고 바로 클래스명.메서드로 사용가능
    # @staticmethod
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()

