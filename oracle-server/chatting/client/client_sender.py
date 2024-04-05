import os
from vidstream import StreamingServer
import threading


def send_file(client, file_path):
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
        
def send_screen():
    try:
        print("Sending screen...")
        receiver = StreamingServer('0.0.0.0', 9999)
        t = threading.Thread(target=receiver.start_server)
        t.start()
        while input("") != 'STOP':
            continue
        receiver.stop_server()
            
    except Exception as e:
        print("An error occurred while sending the screen:", e)