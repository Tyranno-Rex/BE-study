import socket, threading
import os
import client_receiver as cr
import client_sender as cs

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('152.67.212.55', 5000))
# client.connect(('127.0.0.1', 5000))
client.connect(('192.168.3.3', 5000))
nickname = input("Choose your nickname: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                # 파일 수신 준비
                if message == 'FILE RECEIVE READY':
                    cr.receive_file()
                # 원격 화면 공유 수신 준비
                elif message == 'SS START':
                    cr.receive_screen(client)
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = input('')
        if message.strip().lower().startswith('file'):
            cs.send_file(client, "C:/Users/admin/oracle/file.mp4")
        elif message.strip().lower().startswith('screen'):
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))
            cs.send_screen()
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))

# 멀티 클라이언트용 쓰레드
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 메시지 보내기
write_thread = threading.Thread(target=write)
write_thread.start()