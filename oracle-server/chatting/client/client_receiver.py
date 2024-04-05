import os
import time
from vidstream import ScreenShareClient
import threading

def receive_file(client):
    try:
        print("Receiving file...")
        client.send('READY'.encode('ascii'))
        file_size = int(client.recv(1024).decode('ascii'))
        filename = "file"
        client.send('OK'.encode('ascii'))
        received_size = 0
        with open(filename, 'wb') as file:
            while received_size < file_size:
                file_data = client.recv(1024)
                received_size += len(file_data)
                file.write(file_data)
        print("File received successfully.")
    except Exception as e:
        print("An error occurred while receiving the file:", e)
        

def receive_screen(client):
    try:
        print("Receiving screen...")
        ip = client.recv(1024).decode('ascii')
        print(ip)
        time.sleep(2)
        sender = ScreenShareClient(ip, 9999)
        t = threading.Thread(target=sender.start_stream)
        t.start()
    except Exception as e:
        print("An error occurred while receiving the screen:", e)
        