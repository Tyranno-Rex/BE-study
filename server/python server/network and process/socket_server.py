import socket
import random

HOST = ''       # 호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미한다.
PORT = 50008    

# socket.AF_INET: IPv4 프로토콜, socket.SOCK_STREAM: TCP 프로토콜 -> 소켓인 s를 생성한다.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 소켓 s를 주소와 포트에 바인딩한다.
    s.bind((HOST, PORT))
    # 소켓 s를 수동으로 연결 대기 모드로 설정한다.
    s.listen()
    print('서버가 시작되었습니다.')

    # 클라이언트가 접속할 때까지 대기한다.
    # conn: 서버와 클라이언트가 연결된 소켓을 의미한다.
    # addr: 접속이 되면 접속 정보, 즉 클라이언트의 IP주소와 포트번호를 의미한다.
    conn, addr = s.accept()
    with conn:
        answer = random.randint(1, 9)
        print(f'클라이언트가 접속했습니다:{addr}, 정답은 {answer} 입니다.')
        while True:
            # recv: 클라이언트가 보낸 데이터를 수신하는 부분이다.
            # 만약 송신한다면 conn.sendall()을 사용하면 된다.
            # 1024는 한 번에 받을 최대 데이터 사이즈를 의미한다.
            data = conn.recv(1024).decode('utf-8') 

            print(f'데이터:{data}')

            try:
                n = int(data)
            except ValueError:
                conn.sendall(f'입력값이 올바르지 않습니다:{data}'.encode('utf-8'))
                continue

            if n == 0:
                conn.sendall(f"종료".encode('utf-8'))
                break
            if n > answer:
                conn.sendall("너무 높아요".encode('utf-8'))
            elif n < answer:
                conn.sendall("너무 낮아요".encode('utf-8'))
            else:
                conn.sendall("정답".encode('utf-8'))
                break
3