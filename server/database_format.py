import pymysql
import inspect # 호출한 메서드의 이름 가져오기

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
        self.printLogStart()
        result=self.cursor.execute(query, args) # args를 매개변수로 사용하며 SqlInjection방지
        self.printLogEnd()
        return result

    def executeMany(self, query, args=()):
        '''executeMany는 다량의 데이터를 한번에 입력'''
        # args의 매개변수는 리스트의 튜플이 들어가야함
        self.printLogStart()
        result=self.cursor.executemany(query, args)
        self.printLogEnd()
        return result

    def executeOne(self, query, args=()):
        self.printLogStart()
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        self.printLogEnd()
        return row

    def executeAll(self, query, args=()):
        '''쿼리를 실행한뒤(execute) 모든 값을 받아옴(fetchAll)'''
        self.printLogStart()
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        self.printLogEnd()
        return row

    def insertLastKey(self):
        return self.db.insert_id()
    
    def printLogStart(self):
        ''' 쿼리 시작 로그'''
        print("$$$$$ 모델 메소드 시작 => ("+inspect.stack()[2][3]+")$$$$$")

    def printLogEnd(self):
        ''' 쿼리 종료 로그'''
        print("*"*50+"\n")
        print(self.cursor._last_executed) # 쿼리 실행 부분 출력
        print("*"*50)
        print("\n$$$$$ 모델 메소드 종료 => ("+inspect.stack()[2][3]+")$$$$$")

    # 정적메서드_인스턴스화 하지않고 바로 클래스명.메서드로 사용가능
    # @staticmethod
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()
