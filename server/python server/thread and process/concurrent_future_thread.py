import time

def heavy_work(name):
    result = 0
    for i in range(4000000):
        result += i
    print('%s done' % name)
    return result  # 결과를 반환하도록 변경


if __name__ == '__main__':
    import concurrent.futures
    start = time.time()
    total_result = 0
    # 프로세스의 최대 개수를 4로 설정 -> 이는 multiprocessing.Process()와 역할은 같음
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    
    # 4개의 프로세스를 생성하여 heavy_work() 함수를 실행
    thread = []
    for i in range(4):
        thread.append(pool.submit(heavy_work, i))
    
    # 결과를 기다림 / 종료된 순서대로 결과를 가져와서 total_result에 더함
    for p in concurrent.futures.as_completed(thread):
        total_result += p.result()
    end = time.time()
    
    print("수행시간: %f 초" % (end - start))
    print("총결괏값: %s" % total_result)
