import client.handlers as client
import worker.handlers as worker
import multiprocessing
import config as cf
def start():
    worker.start_bot(cf)
def start2():
    client.start_bot(cf)
if __name__=='__main__':
    
    t = multiprocessing.Process(target=start)
    t.start()
    b = multiprocessing.Process(target=start2)
    b.start()
