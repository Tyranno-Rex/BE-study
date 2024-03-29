import time
import multiprocessing
import threading

def heavy_work(name):
    result = 0
    for i in range(40000000):
        result += i
    print('%s done' % name)

class HeavyWork:
    def check_time():
        start = time.time()
        for i in range(4):
            heavy_work(i)
        end = time.time()
        print("수행시간: %f 초" % (end - start))

    def __init__(self):
        HeavyWork.check_time()


class threadProcess:
    def check_time():
        start = time.time()
        threads = []
        for i in range(4):
            t = threading.Thread(target=heavy_work, args=(i, ))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()  # 스레드가 종료될 때까지 대기
        end = time.time()
        print("수행시간: %f 초" % (end - start))
    
    def __init__(self):
        threadProcess.check_time()

class MultiProcess:
    def check_time():
        start = time.time()
        procs = []
        for i in range(4):
            p = multiprocessing.Process(target=heavy_work, args=(i, ))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()  # 프로세스가 모두 종료될 때까지 대기
        end = time.time()
        print("수행시간: %f 초" % (end - start))
    
    def __init__(self):
        MultiProcess.check_time()


if __name__ == '__main__':
    HeavyWork()
    threadProcess()
    MultiProcess()