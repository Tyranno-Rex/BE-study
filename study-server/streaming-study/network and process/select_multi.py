# import socket
# import select
# import random

# HOST = ''
# PORT = 50008

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(5)
#     print('Server started')

#     readsocks = [s]
#     answer = {}

#     while True:
#         # 해당 문장은 select.select() 함수를 사용하여 소켓의 상태를 확인하는 코드이다.
#         # 이벤트가 발생하는 지 감시하는 역할을 한다. 감시하다가 이벤트가 발생하면 해당 이벤트에 대한 처리를 한다.
#         readables, writables, exceptions = select.select(readsocks, [], [])
#         for sock in readables:
#             if sock == s: # 새로운 클라이언트의 요청이 들어온 경우
#                 newsock, addr = s.accept()
#                 answer = random.randint(1, 100)
#                 print('Connected by ', addr, '\nanswer is ', answer)
#                 readsocks.append(newsock)
#                 answer[newsock] = answer
#             else: # 이미 존재하는 클라이언트의 요청이 들어온 경우
#                 conn = sock
#                 data = conn.recv(1024).decode('utf-8')
#                 print('Received: ', data)

#                 try:
#                     n = int(data)
#                 except ValueError:
#                     conn.sendall('plz send a number'.encode('utf-8'))
#                     continue
                
#                 if n == 0:
#                     conn.sendall('bye'.encode('utf-8'))
#                     conn.close()
#                     readsocks.remove(conn)
#                     continue
#                 elif n == answer[conn]:
#                     conn.sendall('correct'.encode('utf-8'))
#                     conn.close()
#                     readsocks.remove(conn)
#                     continue
#                 elif n < answer[conn]:
#                     conn.sendall('bigger'.encode('utf-8'))
#                 else:
#                     conn.sendall('smaller'.encode('utf-8'))

import socket
import select
import random

HOST = ''
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('서버가 시작되었습니다.')

    readsocks = [s]
    answers = {}

    while True:
        # 해당 문장은 select.select() 함수를 사용하여 소켓의 상태를 확인하는 코드이다.
        # 이벤트가 발생하는 지 감시하는 역할을 한다. 감시하다가 이벤트가 발생하면 해당 이벤트에 대한 처리를 한다.
        readables, writeables, excpetions = select.select(readsocks, [], [])
        for sock in readables:
            if sock == s:  # 신규 클라이언트 접속
                newsock, addr = s.accept()
                answer = random.randint(1, 9)
                print(f'클라이언트가 접속했습니다:{addr}, 정답은 {answer} 입니다.')
                readsocks.append(newsock)
                answers[newsock] = answer  # 클라이언트 별 정답 생성
            else:  # 이미 접속한 클라이언트의 요청 (게임진행을 위한 요청)
                conn = sock
                data = conn.recv(1024).decode('utf-8')
                print(f'데이터:{data}')

                try:
                    n = int(data)
                except ValueError:
                    conn.sendall(f'입력값이 올바르지 않습니다:{data}'.encode('utf-8'))
                    continue

                answer = answers.get(conn)
                if n == 0:
                    conn.sendall(f"종료".encode('utf-8'))
                    conn.close()
                    readsocks.remove(conn)  # 클라이언트 접속 해제시 readsocks에서 제거
                if n > answer:
                    conn.sendall("너무 높아요".encode('utf-8'))
                elif n < answer:
                    conn.sendall("너무 낮아요".encode('utf-8'))
                else:
                    conn.sendall("정답".encode('utf-8'))
                    conn.close()
                    readsocks.remove(conn)  # 클라이언트 접속 해제시 readsocks에서 제거
