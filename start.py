import client.handlers as client
import worker.handlers as worker
import threading
import config as cf
print('start')
sql=cf.sql_query
def start():
    print('s1')
    worker.start_bot(cf)
def start2():
    print('s2')

    client.start_bot(cf)
def feedbacks():
    s=sql('SELECT * FROM orders WHERE used=0')
    print(s.fetchall())
t =  threading.Thread(target=start)
t.start()
b =  threading.Thread(target=start2)
b.start()
c =  threading.Thread(target=feedbacks)
c.start()

