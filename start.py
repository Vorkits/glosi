import client.handlers as client
import worker.handlers as worker
import threading
import config as cf
print('start')
def start():
    print('s1')
    worker.start_bot(cf)
def start2():
    print('s2')

    client.start_bot(cf)

t =  threading.Thread(target=start)
t.start()
b =  threading.Thread(target=start2)
b.start()
