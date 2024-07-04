from flask import Flask, jsonify, request, Response
import cv2, os
import socket, threading, sys, requests
import signal

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










def generate_frames(video_path):
    video = cv2.VideoCapture(video_path)
    while True:
        success, frame = video.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 동영상 이름도 받아 올거임
@app.route('/video_feed')
def video_feed():
    video_name = request.args.get('video_name')
    video_path = 'C:/Users/admin/project/oracle/oracle-server/h264/database/' + video_name
    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_frame_count')
def get_frame_count():
    video_name = request.args.get('video_name')
    video_path = 'C:/Users/admin/project/oracle/oracle-server/h264/database/' + video_name
    video = cv2.VideoCapture(video_path)
    frame_count = video.get(cv2.CAP_PROP_FPS)
    return {'frame_count': frame_count}

@app.route('/get_video_list')
def get_video_list():
    video_list = os.listdir('C:/Users/admin/project/oracle/oracle-server/h264/database')
    return {'video_list': video_list}





# Flask 서버 시작
if __name__ == '__main__':
    sv = Server()
    thread = threading.Thread(target=sv.receive)
    thread.start()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)