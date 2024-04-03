import socket, threading
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('152.67.212.55', 5000))
client.connect(('127.0.0.1', 5000))
nickname = input("Choose your nickname: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def send_file(file_path):
    try:
        print("Sending file...")
        client.send('file'.encode('ascii'))
        file_size = os.path.getsize(file_path)
        # 파일 크기 전송
        client.send(str(file_size).encode('ascii'))
        # 파일 데이터 전송
        message = client.recv(1024).decode('ascii')
        if (message == 'OK'):
            with open(file_path, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    print(file_data)
                    if not file_data:
                        break
                    client.sendall(file_data)
            print("File sent successfully.")
        else:
            print("An error occurred while sending the file.")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred while sending the file:", e)

def write():
    while True:
        message = input('')
        if message.strip().lower().startswith('textfile'):
            send_file("C:\\Users\\admin\\oracle-client\\video.mp4")
            # send_file("C:\\Users\\admin\\oracle-client\\images.jpg")
            # send_file("C:\\Code\\streaming-server\\test\\text.txt")
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))

# 멀티 클라이언트용 쓰레드
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 메시지 보내기
write_thread = threading.Thread(target=write)
write_thread.start()
