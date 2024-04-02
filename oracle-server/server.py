from flask import Flask, jsonify
import socket, threading, sys, requests
import signal, json

app = Flask(__name__)

host = '0.0.0.0'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
commander = []
nicknames = []

class Server:
    def __init__(self):
        self.broadcast = self.broadcast
        self.handle = self.handle
        self.receive = self.receive
    
    def broadcast(self, message):
        for client in clients:
            client.send(message)
    
    def send_query(self, query):
        url = "http://158.180.80.199:5000/execute_query"
        data = {'query': query}
        response = requests.get(url, json=data)
        if (response.status_code == 200):
            return response.json()
        else:
            return {"error": "Failed to execute query"}

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                
                if message.decode('ascii').find('query') != -1:
                    # sql 뒤에 오는 문장은 sql 쿼리로 인식
                    query = message.decode('ascii').split('query ')[1]
                    result = json.dumps(self.send_query(query))
                    self.broadcast(result.encode('ascii'))
                else:
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
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)