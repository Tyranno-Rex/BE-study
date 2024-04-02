import socket, threading
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))
nickname = input("Choose your nickname: ")



def getFileSize(file):
    return os.path.getsize(file)

def getFileData(file_t):
    with open(file_t, 'rb') as file:  # 인코딩 인자 제거
        data = b""  # 이진 데이터로 저장
        for line in file:
            data += line
    return data

def send_file(file_path):
    try:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        # 파일 정보 전송
        client.send(f"file {file_name}".encode('ascii'))
        client.recv(1024)  # 서버가 준비되었다는 응답을 받음
        client.send(str(file_size).encode('ascii'))
        # 파일 데이터 전송
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client.send(data)
                data = file.read(1024)
        print("File sent successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred while sending the file:", e)


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Ready to receive file':
                send_file("/home/oracle/oracle-server/text.txt")
            elif message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# 멀티 클라이언트용 쓰레드
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 메시지 보내기
write_thread = threading.Thread(target=write)
write_thread.start()