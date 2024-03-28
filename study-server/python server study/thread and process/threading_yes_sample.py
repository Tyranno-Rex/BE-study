import urllib.request


def get_wikidocs(page):
    print("wikidocs page:{}".format(page))  # 페이지 호출시 출력
    resource = 'https://wikidocs.net/{}'.format(page)
    try:
        with urllib.request.urlopen(resource) as s:
            with open('wikidocs_%s.html' % page, 'wb') as f:
                f.write(s.read())
    except urllib.error.HTTPError:
        return 'Not Found'


import time
import threading

start = time.time()

pages = [12, 13, 14, 15, 17, 18, 20, 21, 22, 24]
threads = []
for page in pages:
    # 스레드 생성
    t = threading.Thread(target=get_wikidocs, args=(page, ))
    # 스레드가 독립적으로 실행됨
    t.start()
    # 여기서 바로 join을 하면 스레드의 독립적인 실행이 의미가 없어짐
    # 때문에 스레드를 리스트에 저장해놓고 나중에 join을 실행
    threads.append(t)

for t in threads:
    # 스레드가 종료될 때까지 대기
    t.join()  

end = time.time()

print("수행시간: %f 초" % (end - start))
