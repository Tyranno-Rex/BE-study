from flask import Flask, jsonify
import socket, threading, sys, requests
import signal, json
from collections import deque

import server_function as sf
import server_message_handler as smh

app = Flask(__name__)

host = '0.0.0.0'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
room_list = []

class Server:
    def __init__(self):
        self.sender = self.sender
        self.receive = self.receive

    def sender(self, client):
        while True:
            try:
                message = client.recv(1024)
                smh.message_handler(client, clients, message, room_list, nicknames)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                sf.broadcast_all(clients, "{} left!\n".format(nickname).encode('ascii'))
                sf.broadcast_all(clients, "{} people in this room!\n".format(len(nicknames)).encode('ascii'))
                nicknames.remove(nickname)
                break
    
    def receive(self):
        while True:
            # 클라이언트 연결 수락
            client, address = server.accept()
            print("Connected with {}".format(str(address)))
            
            client.send('NICKNAME'.encode('ascii'))

            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)
            
            print("Nickname is {}".format(nickname))
            sf.broadcast_all(clients, "{} joined!\n".format(nickname).encode('ascii'))
            sf.broadcast_all(clients, "{} people in this room!\n".format(len(nicknames)).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            
            thread = threading.Thread(target=self.sender, args=(client,))
            thread.start()

# Ctrl+C 시그널 핸들러
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    server.close()  # 서버 소켓 닫기
    sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

# Flask 서버 시작
if __name__ == '__main__':
    sv = Server()
    thread = threading.Thread(target=sv.receive)
    thread.start()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)