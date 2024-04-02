from flask import Flask, jsonify
import socket, threading, sys, requests
import signal, json
from collections import deque

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
        self.broadcast = self.broadcast
        self.handle = self.handle
        self.receive = self.receive
    
    def broadcast(self, message):
        for client in clients:
            client.send(message)
    
    def broadcast_in_room(self, message, room):
        for client in room["clients"]:
            client.send(message)
    
    def send_query(self, query):
        url = "http://158.180.80.199:5000/execute_query"
        data = {'query': query}
        response = requests.get(url, json=data)
        if (response.status_code == 200):
            return response.json()
        else:
            return {"error": "Failed to execute query"}
    
    def receive_file(client, message):
        print("start receive file")
        client.send('Ready to receive file'.encode('ascii'))
        filename = message.decode('ascii').split('file ')[1]
        client.send('Ready to receive file size'.encode('ascii'))
        file_size = client.recv(1024).decode('ascii')
        print("Receiving file {} with size {}".format(filename, file_size))
        received_size = 0
        with open(filename, 'wb') as file:
            while received_size < int(file_size):
                file_data = client.recv(1024)
                received_size += len(file_data)
                file.write(file_data)
        print("File received successfully.")

    def message_handler(self, client, message):
        # 쿼리 진행
        if message.decode('ascii').find('query') != -1:
            # sql 뒤에 오는 문장은 sql 쿼리로 인식
            query = message.decode('ascii').split('query ')[1]
            result = json.dumps(self.send_query(query))
            self.broadcast(result.encode('ascii'))
        
        # 방 생성
        if message.decode('ascii').find('room') != -1:
            # room 뒤에 오는 문장은 방 이름으로 인식
            room = message.decode('ascii').split('room ')[1]
            if (room not in room_list):
                room = {"room": room, "clients": []}
                room["clients"].append(client)
                room_list.append(room)
                self.broadcast("Room {} is created!\n".format(room).encode('ascii'))
            else:
                self.broadcast("Room {} is already created!\n".format(room).encode('ascii'))
        
        # 방 참여
        if message.decode('ascii').find('join') != -1:
            room = message.decode('ascii').split('join ')[1]
            for r in room_list:
                if (r["room"] == room):
                    r["clients"].append(client)
                    self.broadcast_in_room("Someone joined room {}!\n".format(room).encode('ascii'), r)
                    break
        
        # 방 나가기
        if message.decode('ascii').find('leave') != -1:
            room = message.decode('ascii').split('leave ')[1]
            for r in room_list:
                if (r["room"] == room):
                    r["clients"].remove(client)
                    self.broadcast_in_room("Someone left room {}!\n".format(room).encode('ascii'), r)
                    break
        
        # 방 대화
        if message.decode('ascii').find('talk') != -1:
            msg = message.decode('ascii').split('talk ')[1]
            for r in room_list:
                if (client in r["clients"]):
                    self.broadcast_in_room(msg.encode('ascii'), r)

        if message.decode('ascii').find('file') != -1:
            print("djaklsdfjaklsfj")
            receive_file(client, message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.message_handler(client, message)
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
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)