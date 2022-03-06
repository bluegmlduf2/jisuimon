bind = '127.0.0.1:5000'
backlog = 2048

workers = 8
worker_class = 'sync'
worker_connections = 1000
timeout = 120 # 이미지 업로드시 타임아웃되어서 에러가 뜨기 때문에 30->120초 수정
keepalive = 2

umask = 0
errorlog = '-' # 에러로그 출력하는곳 현재상태는 콘솔에출력
loglevel = 'info'
accesslog = '-' # 접속로그 출력하는곳 현재상태는 콘솔에출력
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'