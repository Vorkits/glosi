import client.handlers as client
import worker.handlers as worker
import multiprocessing
import config as cf
print('start')
def start():
    print('s1')
    worker.start_bot(cf)
def start2():
    print('s2')

    client.start_bot(cf)

t = multiprocessing.Process(target=start)
t.start()
b = multiprocessing.Process(target=start2)
b.start()
