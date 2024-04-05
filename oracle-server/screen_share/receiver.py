from vidstream import  ScreenShareClient
import threading

sender = ScreenShareClient('192.168.3.3', 9999)
# sender = ScreenShareClient('127.0.0.1', 9999)

t = threading.Thread(target=sender.start_stream)
t.start()

while input("") != 'STOP':
    continue

sender.stop_stream()