from flask import Flask, jsonify
import socket, threading, sys, requests
import signal, json

app = Flask(__name__)

host = '127.0.0.1'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

class_list = []
class_joiner = []

class Server:
    def __init__(self):
        self.broadcast = self.broadcast
        self.handle = self.handle
        self.receive = self.receive
        
        
    def get_lecture_info(self, client, questions):
        answers = []
        for question in questions:
            client.send(question.encode('ascii'))
            answer = client.recv(1024).decode('ascii')
            answers.append(answer)
        return answers
    
    def broadcast(self, message):
        for client in clients:
            client.send(message)
            
            
    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                self.broadcast("{} left!\n".format(nickname).encode('ascii'))
                self.broadcast("{} people in this room!\n".format(len(nicknames)).encode('ascii'))
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
            self.broadcast("{} joined!\n".format(nickname).encode('ascii'))
            self.broadcast("{} people in this room!\n".format(len(nicknames)).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            
            
            thread = threading.Thread(target=self.handle, args=(client,))
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
    app.run(debug=True, threaded=True, port=5000)